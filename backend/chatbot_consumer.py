from confluent_kafka import Consumer, Producer
import json, time

KAFKA_BROKER = 'localhost:9092'
MESSAGE_TOPIC = 'chat_messages'
RESPONSE_TOPIC = 'bot_responses'

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'chatbot-group',
    'auto.offset.reset': 'earliest'
}

producer_conf = {
    'bootstrap.servers': KAFKA_BROKER
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe([MESSAGE_TOPIC])

print('🤖 Chatbot processor started — listening on topic "chat_messages"...')

def generate_reply(text):
    text = text.lower()
    if 'time' in text:
        return f"The current time is {time.strftime('%H:%M:%S')}."
    elif 'hello' in text or 'hi' in text:
        return "Hello there 👋, how can I help you today?"
    elif 'thanks' in text or 'thank you' in text:
        return "You're most welcome 😊"
    elif 'bye' in text:
        return "Goodbye 👋! Have a great day!"
    else:
        return "I'm not sure I understand yet, but I'm learning!"

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"⚠️ Error: {msg.error()}")
        continue

    data = json.loads(msg.value().decode('utf-8'))
    user = data.get('user', 'Guest')
    message = data.get('message', '')

    print(f"[processor] Received from {user}: {message}")

    # Generate bot reply
    reply = generate_reply(message)
    bot_response = {
        'bot': 'KafkaBot',
        'reply': reply,
        'timestamp': time.time()
    }

    # Send bot reply to Kafka
    producer.produce(RESPONSE_TOPIC, json.dumps(bot_response).encode('utf-8'))
    producer.flush()

    print(f"[bot] Sent reply: {reply}")


consumer.close()
