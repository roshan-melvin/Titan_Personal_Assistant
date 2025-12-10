import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "0.tcp.in.ngrok.io"
MQTT_PORT = 17998
MQTT_TOPIC = "test_sensor_data"

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT broker successfully")
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}")

def ring_buzzer():
    """Send a command to ring the smoke detector buzzer via MQTT."""
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(0.5)  # Give time for connection
        client.publish(MQTT_TOPIC, "RING_BUZZER")
        print("Publishing buzzer command...")
        time.sleep(0.5)  # Give time for message to send
        client.loop_stop()
        client.disconnect()
        return True
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return False    