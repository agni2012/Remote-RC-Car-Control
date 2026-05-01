import asyncio
from flask import Flask
from bleak import BleakScanner, BleakClient
import threading

# --- Configuration ---
HUB_NAME = "depth bot"
CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

app = Flask(__name__)
loop = asyncio.new_event_loop()
client = None

# This runs the Bluetooth logic in the background
def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def connect_to_car():
    global client
    print(f"Searching for {HUB_NAME}...")
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if device:
        client = BleakClient(device)
        await client.connect()
        print("Connected to Mars Rover!")
    else:
        print("Car not found.")

async def send_cmd(char):
    if client and client.is_connected:
        # Prepend 0x06 for write stdin
        await client.write_gatt_char(CHAR_UUID, b"\x06" + char.encode(), response=True)

# --- Web Routes ---

@app.route('/control/<cmd>')
def control(cmd):
	#    # Map the long strings to single special characters
	#    mapping = {
	#        'xws': 'f', # Forward/Back stop
	#        'xad': 'h', # Left/Right stop
	#        'xrg': 'j'  # Motor C stop
	#    }
    
    # Use the mapped character if it exists, otherwise use the raw cmd
    final_cmd = cmd.lower()

    # Update valid list to include our new single-char codes
    if final_cmd in ['w', 'a', 's', 'd', 'r', 'g', 'x', 'f', 'h', 'j']:
        asyncio.run_coroutine_threadsafe(send_cmd(final_cmd), loop)
        return f"Sent {final_cmd}", 200
    return "Invalid Command", 400
if __name__ == "__main__":
    # Start the Bluetooth thread
    threading.Thread(target=run_async_loop, args=(loop,), daemon=True).start()
    asyncio.run_coroutine_threadsafe(connect_to_car(), loop)
    
    # Start the Web Server
    # host='0.0.0.0' makes it accessible on your local network
    app.run(host='0.0.0.0', port=5000)
