import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('Guest');
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:5000/responses');
        const data = await res.json();
        setChat(data);
      } catch (e) {
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const send = async () => {
    if (!message) return;
    await fetch('http://localhost:5000/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, message })
    });
    setMessage('');
  };

  return (
    <div className="app">
      <h2>Kafka Chatbot</h2>
      <div className="controls">
        <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Your name" />
      </div>
      <div className="chat-area">
        {chat.map((c, i) => (
          <div key={i} className="chat-line">
            <strong>{c.bot || 'Bot'}</strong>: {c.reply}
          </div>
        ))}
      </div>
      <div className="composer">
        <input value={message} onChange={e => setMessage(e.target.value)} onKeyDown={e => { if(e.key==='Enter') send(); }} placeholder="Type a message" />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}

export default App;
