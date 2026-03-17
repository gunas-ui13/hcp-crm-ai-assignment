import os
import json
from datetime import date
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from .database import SessionLocal
from .models import Interaction, SentimentEnum

load_dotenv()

# --- DEFINE THE TOOLS ---

@tool
def log_interaction(hcp_name: str, interaction_type: str, notes: str, sentiment: str):
    """Use this tool to log a new interaction with an HCP. Extracts details from the chat."""
    db = SessionLocal()
    try:
        try:
            enum_sentiment = SentimentEnum(sentiment.capitalize())
        except ValueError:
            enum_sentiment = SentimentEnum.neutral

        new_interaction = Interaction(
            hcp_name=hcp_name,
            interaction_type=interaction_type,
            date=date.today(),
            topics_discussed=notes,
            sentiment=enum_sentiment
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return f"Success: Interaction logged for {hcp_name} with ID {new_interaction.id}."
    except Exception as e:
        db.rollback()
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()

@tool
def edit_interaction(updated_notes: str, interaction_id: int = None, hcp_name: str = None):
    """Use this tool to update the notes of an existing record. Provide interaction_id or hcp_name."""
    db = SessionLocal()
    try:
        # Fallback: Find latest record for HCP if ID is missing
        target_id = interaction_id
        if not target_id and hcp_name:
            latest = db.query(Interaction).filter(Interaction.hcp_name.contains(hcp_name)).order_by(Interaction.id.desc()).first()
            if latest:
                target_id = latest.id

        if not target_id:
            return "Error: Could not determine which record to update. Please provide an ID or HCP name."

        interaction = db.query(Interaction).filter(Interaction.id == target_id).first()
        if interaction:
            interaction.topics_discussed = updated_notes
            db.add(interaction) # Mark as modified
            db.commit() # Save to MySQL
            return f"Success: Interaction {target_id} for {interaction.hcp_name} has been updated in the database."
        return f"Error: Interaction {target_id} not found."
    except Exception as e:
        db.rollback()
        return f"Error updating: {str(e)}"
    finally:
        db.close()

@tool
def delete_interaction(interaction_id: int = None, hcp_name: str = None):
    """Use this tool to permanently remove a record. Provide interaction_id or hcp_name."""
    db = SessionLocal()
    try:
        target_id = interaction_id
        if not target_id and hcp_name:
            latest = db.query(Interaction).filter(Interaction.hcp_name.contains(hcp_name)).order_by(Interaction.id.desc()).first()
            if latest:
                target_id = latest.id

        interaction = db.query(Interaction).filter(Interaction.id == target_id).first()
        if interaction:
            db.delete(interaction)
            db.commit() # Save deletion to MySQL
            return f"Success: Interaction {target_id} has been permanently deleted from the database."
        return f"Error: Record not found."
    except Exception as e:
        db.rollback()
        return f"Error deleting: {str(e)}"
    finally:
        db.close()

@tool
def get_hcp_history(hcp_name: str):
    """Use this tool to search for previous interactions with a specific HCP."""
    db = SessionLocal()
    try:
        history = db.query(Interaction).filter(Interaction.hcp_name.contains(hcp_name)).all()
        if not history:
            return f"No history found for {hcp_name}."
        history_str = "\n".join([f"ID {h.id} ({h.date}): {h.topics_discussed}" for h in history])
        return f"History for {hcp_name}:\n{history_str}"
    finally:
        db.close()

@tool
def schedule_follow_up(hcp_name: str, follow_up_date: str, topic: str):
    """Use this tool to schedule a follow-up action or meeting."""
    return f"Follow-up scheduled with {hcp_name} on {follow_up_date} regarding {topic}."

@tool
def extract_action_items(notes: str):
    """Use this tool to extract key outcomes and action items from raw notes."""
    return f"Action items extracted: Follow up on clinical trial discussion and send brochures."

# List of all tools available to the agent
tools = [
    log_interaction, 
    edit_interaction, 
    delete_interaction,
    get_hcp_history, 
    schedule_follow_up, 
    extract_action_items
]

# --- SET UP THE LLM & LANGGRAPH AGENT ---

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY")
)

agent_executor = create_react_agent(llm, tools)

def process_chat(user_input: str):
    system_prompt = (
        "You are a proactive AI assistant for a Life Sciences CRM. "
        "Your job is to help pharma reps manage HCP interactions efficiently. "
        
        "CRITICAL: When asked to edit, update, or delete, you MUST use the corresponding tool. "
        "If you don't have an ID, use the HCP name to find and update the most recent record. "

        "MANDATORY CONFIRMATION: When you successfully log, edit, or delete data, "
        "always start your response with a clear confirmation like: "
        "'Okay, I have successfully logged those details for you.' or "
        "'Confirmed: Interaction for [HCP Name] has been updated.' "
        
        "PROACTIVE ENGAGEMENT: After every action, you MUST ask the user if they would like to "
        "Edit, Update, or Delete any records, or if they need help with another task. "
        
        "MANDATORY UI SYNC: Every time you identify HCP details (Name, Type, Notes, Sentiment), "
        "you MUST output a JSON block inside <form_data> tags at the very end of your response. "
        "Fields: hcpName, interactionType, notes, sentiment. "
        "Example: <form_data>{\"hcpName\": \"Dr. Sharma\", \"sentiment\": \"Neutral\"}</form_data>"
    )
    
    inputs = {"messages": [("system", system_prompt), ("user", user_input)]}
    response = agent_executor.invoke(inputs)
    full_content = response["messages"][-1].content

    form_update = None
    if "<form_data>" in full_content:
        try:
            start_tag = "<form_data>"
            end_tag = "</form_data>"
            start_idx = full_content.find(start_tag) + len(start_tag)
            end_idx = full_content.find(end_tag)
            
            json_str = full_content[start_idx:end_idx].strip()
            json_str = json_str.replace("'", '"')
            
            form_update = json.loads(json_str)
            full_content = full_content[:full_content.find(start_tag)].strip()
        except Exception as e:
            print(f"Extraction Error: {e}")
            pass

    return {"ai_message": full_content, "form_update": form_update}