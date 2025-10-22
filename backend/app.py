from flask import Flask, request, jsonify
from confluent_kafka import Producer, Consumer
import threading, json, time, uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KAFKA_BROKER = 'localhost:9092'
MESSAGE_TOPIC = 'chat_messages'
RESPONSE_TOPIC = 'bot_responses'

producer = Producer({'bootstrap.servers': KAFKA_BROKER})
responses = []

def consume_responses():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'web-consumer-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([RESPONSE_TOPIC])
    while True:
        msg = consumer.poll(1.0)
        if msg and not msg.error():
            try:
                payload = json.loads(msg.value().decode('utf-8'))
                print(f"[Flask] Received from bot: {payload}") 
                responses.append(payload)
                if len(responses) > 1000:
                    responses.pop(0)
            except Exception:
                continue

threading.Thread(target=consume_responses, daemon=True).start()

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json or {}
    username = data.get('username', 'Guest')
    message = data.get('message', '')
    msg_data = {
        'id': str(uuid.uuid4()),
        'user': username,
        'message': message,
        'timestamp': time.time()
    }
    producer.produce(MESSAGE_TOPIC, json.dumps(msg_data).encode('utf-8'))
    producer.flush()
    return jsonify({'status': 'sent'})

@app.route('/responses', methods=['GET'])
def get_responses():
    return jsonify(responses[-200:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
