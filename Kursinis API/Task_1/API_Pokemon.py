from flask import Flask, jsonify, send_file, render_template
import requests
import json
import paho.mqtt.client as mqtt
from flask_mqtt import Mqtt as FMQTT

mqttBroker = "broker.mqttdashboard.com"
topic = "Lukas/Pokemon"

app = Flask(__name__)

# Set up Flask-MQTT
app.config['MQTT_BROKER_URL'] = mqttBroker
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
mqtt = FMQTT(app)

def jprint(data):
    # create a formatted string of the Python JSON object
    text = json.dumps(data, sort_keys=True, indent=4)
    print(text)

@app.route('/')
def get_pokemon_potd():
    url = "https://pokeapi.deno.dev/pokemon/potd"
    response = requests.get(url)
    data = response.json()
    jprint(data)

    with open('pokemon_potd.json', 'w') as f:
        json.dump(data, f)

    print("Connecting to MQTT broker...")
    mqtt.publish(topic, json.dumps(data))
    print("Published to topic:", topic)

    return render_template('pokemon.html', pokemon=data)

@app.route('/download')
def send_pokemon_potd():
    return send_file('pokemon_potd.json', as_attachment=True)


if __name__ == '__main__':
    app.run()
