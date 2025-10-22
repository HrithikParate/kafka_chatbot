# producer.py - Confluent Kafka version
from confluent_kafka import Producer
import json, time, socket, uuid

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

username = input("Enter your name: ").strip() or socket.gethostname()
topic = "chat_messages"

def delivery_report(err, msg):
    if err:
        print('Message delivery failed:', err)

print("Type messages and press Enter. Type 'exit' to quit.")
while True:
    msg = input(f"{username}: ").strip()
    if not msg:
        continue
    if msg.lower() == 'exit':
        break
    data = {
        "id": str(uuid.uuid4()),
        "user": username,
        "message": msg,
        "timestamp": time.time()
    }
    producer.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()
