#I would normally use Node, but the PB docs was all python, idk why.
import asyncio
from flask import Flask
from bleak import BleakScanner, BleakClient
import threading

# NOTE: pls change this to the correct hub!!
HUB_NAME = "depth bot"
CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef" #dont even ask

app = Flask(__name__)
loop = asyncio.new_event_loop()
client = None

# ble logic in background
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
		#Im sorry gods, i vibe coded some of this
        await client.write_gatt_char(CHAR_UUID, b"\x06" + char.encode(), response=True)
#This sholud be done in node!!!!!
@app.route('/control/<cmd>')
def control(cmd):

    final_cmd = cmd.lower()
    if final_cmd in ['w', 'a', 's', 'd', 'r', 'g', 'x', 'f', 'h', 'j']:
        asyncio.run_coroutine_threadsafe(send_cmd(final_cmd), loop)
        return f"Sent {final_cmd}", 200
    return "Client, stop hacking, thats not a valid command", 400
if __name__ == "__main__":
    threading.Thread(target=run_async_loop, args=(loop,), daemon=True).start()
    asyncio.run_coroutine_threadsafe(connect_to_car(), loop)
    app.run(host='0.0.0.0', port=5000)
