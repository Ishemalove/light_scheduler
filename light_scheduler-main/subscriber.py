import paho.mqtt.client as mqtt
import serial
import serial.tools.list_ports
import time
import os

# Serial port configuration
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description or 'USB Serial' in port.description:
            return port.device
    return None

SERIAL_PORT = find_arduino_port()
if SERIAL_PORT is None:
    print("Error: No Arduino found. Please connect your Arduino and try again.")
    print("Available ports:", [port.device for port in serial.tools.list_ports.comports()])
    exit(1)

BAUD_RATE = 9600
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    print(f"Connected to Arduino on {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    exit(1)

# MQTT configuration
MQTT_BROKER = '157.173.101.159'
MQTT_PORT = 1883
MQTT_TOPIC = 'relay/schedule'
COMMAND_FILE = 'relay.txt'

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    command = msg.payload.decode().strip()
    print(f"Received MQTT message: {command} at {time.strftime('%H:%M')}")
    with open(COMMAND_FILE, 'w') as f:
        f.write(command)
    if command == '1':
        ser.write(b"ON\n")
        print(f"Sent to Arduino: ON at {time.strftime('%H:%M')}")
    elif command == '0':
        ser.write(b"OFF\n")
        print(f"Sent to Arduino: OFF at {time.strftime('%H:%M')}")
    else:
        print(f"Unknown command received: {command}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Stopping...")
    client.loop_stop()
    client.disconnect()
    ser.close()