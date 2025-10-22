Kafka Chatbot — Full stack

Structure:
  backend/
    app.py
    producer.py
    chatbot_consumer.py
    requirements.txt
    docker-compose.yml

  frontend/
    package.json
    src/
      App.js
      index.js
      App.css
    public/
      index.html

Quick start:
  1. Start Kafka (Redpanda):
     cd backend
     docker-compose up -d

  2. Install backend deps and run Flask:
     pip install -r requirements.txt
     python app.py

  3. Start frontend:
     cd frontend
     npm install
     npm start
     Open http://localhost:3000
