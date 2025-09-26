from mqtt_pubsub import MQTTSubscriber

def handle_message(topic, message):
    print(f"[Subscriber] Received from {topic}: {message}")

sub = MQTTSubscriber(topic="Floor")
sub.connect()
sub.set_on_message(handle_message)
sub.subscribe()

# Keep alive
while True:
    pass
