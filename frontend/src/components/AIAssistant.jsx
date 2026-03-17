import React, { useState } from 'react';
import { Bot, Send, Loader2 } from 'lucide-react';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { updateField } from '../store/interactionSlice';

const AIAssistant = () => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Log interaction details here or ask for help.' }
  ]);
  
  const dispatch = useDispatch();

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    // Add user message to state
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/chat', {
        message: userMessage
      });

      // Extract the data from the new backend structure
      const { ai_message, form_update } = res.data.response;

      // Add AI response to state
      setMessages((prev) => [...prev, { role: 'assistant', content: ai_message }]);

      // Sync form fields to Redux
      if (form_update) {
        Object.keys(form_update).forEach((field) => {
          dispatch(updateField({ field, value: form_update[field] }));
        });
      }

    } catch (error) {
      console.error(error);
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Sorry, I encountered a connection error.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>
        <Bot size={20} color="#3b82f6" />
        <span style={{ fontWeight: '600' }}>AI Assistant</span>
      </div>

      {/* CHAT AREA */}
      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px', padding: '5px' }}>
        {messages.map((msg, i) => (
          <div 
            key={i} 
            style={{ 
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.role === 'user' ? '#3b82f6' : '#f1f5f9',
              color: msg.role === 'user' ? 'white' : '#1e293b',
              padding: '10px 14px',
              borderRadius: msg.role === 'user' ? '15px 15px 2px 15px' : '15px 15px 15px 2px',
              maxWidth: '80%',
              fontSize: '0.9rem',
              boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
            }}
          >
            {msg.content}
          </div>
        ))}
        {isLoading && <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>AI is thinking...</div>}
      </div>

      {/* INPUT AREA */}
      <form onSubmit={handleSend} style={{ display: 'flex', gap: '8px', marginTop: '15px' }}>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe interaction..." 
          style={{ flex: 1, padding: '10px', borderRadius: '8px', border: '1px solid #ddd' }}
        />
        <button 
          type="submit" 
          style={{ backgroundColor: '#3b82f6', color: 'white', border: 'none', borderRadius: '8px', padding: '0 12px', cursor: 'pointer' }}
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};

export default AIAssistant;