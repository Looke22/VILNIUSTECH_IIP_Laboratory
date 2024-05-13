import requests
import json
import paho.mqtt.client as mqtt

mqttBroker = "broker.mqttdashboard.com"
topic = "Lukas/Pokemon"

def scrape_pokemon_potd():
    url = "https://pokeapi.deno.dev/pokemon/potd"
    response = requests.get(url)
    data = response.json()
    return data

def send_to_mqtt(data):
    client = mqtt.Client()
    client.connect(mqttBroker)
    client.publish(topic, json.dumps(data))
    client.disconnect()

def main():
    pokemon_potd_data = scrape_pokemon_potd()
    if pokemon_potd_data:
        send_to_mqtt(pokemon_potd_data)

if __name__ == "__main__":
    main()
