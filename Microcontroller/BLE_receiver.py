# from bleson import get_provider, Observer, UUID16
# from time import sleep

# def on_advertisement(advertisement):
#     print(advertisement)
#     mfg_data = advertisement.mfg_data
#     address = advertisement.address

#     if mfg_data is not None:
#         print("-" * 50, "Advert", "-"*50)
#         print(f"""
#           Device Name: {advertisement._name}
#           Address: {advertisement.address_type}: {advertisement.address}
#           Raw:{advertisement.raw_data} \t Raw Hex:{advertisement.raw_data.hex()}
#           Mgf Date: {advertisement.mfg_data}        
#         """)

# adapter = get_provider().get_adapter()

# observer = Observer(adapter)
# observer.on_advertising_data = on_advertisement

# observer.start()
# while True:
#     sleep(10)

# observer.stop()

import asyncio
from bleak import BleakScanner, BleakClient

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)



loop = asyncio.get_event_loop()
loop.run_until_complete(run())

#connect to device with address
address = "D8:3A:DD:5C:49:AC:"
MODEL_NBR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E" #this is the UUID for the characteristic that we want to read, 

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))
