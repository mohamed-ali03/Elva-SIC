import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker="broker.hivemq.com", port=1883, topic="elevator/test", client_id=""):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(client_id)

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def publish(self, message):
        """Publish a message to the topic."""
        self.client.publish(self.topic, message)
        print(f"[Publisher] Sent: {message}")


class MQTTSubscriber:
    def __init__(self, broker="broker.hivemq.com", port=1883, topic="elevator/test", client_id=""):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(client_id)
        self.on_message_callback = None

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def set_on_message(self, callback):
        """Set callback for received messages."""
        self.on_message_callback = callback
        self.client.on_message = self._internal_on_message

    def _internal_on_message(self, client, userdata, msg):
        if self.on_message_callback:
            self.on_message_callback(msg.topic, msg.payload.decode())

    def subscribe(self):
        """Subscribe to topic and listen in background."""
        self.client.subscribe(self.topic)
        self.client.loop_start()
