import React from 'react';
import InteractionForm from './components/InteractionForm';
import AIAssistant from './components/AIAssistant';

function App() {
  return (
    <div className="app-container">
      {/* Left Side: The Form */}
      <div className="form-panel">
        <InteractionForm />
      </div>

      {/* Right Side: The AI Chat */}
      <div className="chat-panel">
        <AIAssistant />
      </div>
    </div>
  );
}

export default App;