from sqlalchemy import Column, Integer, String, Date, Time, Text, Enum
from .database import Base
import enum

# Define the sentiment options based on the UI provided in the PDF
class SentimentEnum(str, enum.Enum):
    positive = "Positive"
    neutral = "Neutral"
    negative = "Negative"

# This represents the 'interactions' table in your database
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), index=True)
    interaction_type = Column(String(100))
    date = Column(Date)
    time = Column(Time)
    attendees = Column(Text, nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(Text, nullable=True)
    samples_distributed = Column(Text, nullable=True)
    sentiment = Column(Enum(SentimentEnum), default=SentimentEnum.neutral)
    outcomes = Column(Text, nullable=True)
    follow_up_actions = Column(Text, nullable=True)