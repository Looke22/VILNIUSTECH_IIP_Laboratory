from flask import Flask, render_template
import paho.mqtt.client as mqtt
from flask_mqtt import Mqtt as FMQTT
import json

app = Flask(__name__)

broker_address = "broker.mqttdashboard.com"
port = 1883
topic = "Lukas/Pokemon"
client_id = "Lukas_mqtt_to_flask"

# Set up Flask-MQTT
app.config['MQTT_BROKER_URL'] = broker_address
app.config['MQTT_BROKER_PORT'] = port
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
mqttApp = FMQTT(app)

json_payload = None  # Initialize JSON payload as None

def on_message(client, userdata, message,):
    global json_payload
    json_payload = json.loads(message.payload.decode("utf-8"))

@app.route('/')
def display_pokemon_info():
    if json_payload:
        return render_template('pokemon.html', pokemon=json_payload)
    else:
        return "Waiting for MQTT message..."

if __name__ == '__main__':
    client = mqtt.Client(client_id)
    client.on_message = on_message
    client.connect(broker_address, port)
    client.subscribe(topic)
    client.loop_start()  # Start MQTT client loop in a separate thread
    app.run()
