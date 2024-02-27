import paho.mqtt.client as mqtt
import time

def connect_broker(broker_address, client_name):
    client = mqtt.Client(client_name)
    client.connect(broker_address)
    time.sleep(1)
    client.loop_start()
    
    return client

if __name__ == "__main__":
    server = "broker.emqx.io"
    client_name = "Looke22"
    client = connect_broker(server, client_name)
    
    try:
        while True:
            message = input('Send some random message:')
            client.publish("temperature/kambarys2", message)
            
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
