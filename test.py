from NSF_Soft_Sensor import FlexSense_Bluetooth
import asyncio

async def main():
    ble = FlexSense_Bluetooth()
    await ble.connect("FlexibleSensorBLE")
    async def callback(characteristic, d : bytearray):
        print(d)
    await ble.capture("eb523251-6513-11ed-9c9d-0800200c9a66".format(0xFFE1), callback)
    await asyncio.sleep(2)
    await ble.endCapture()
    await ble.disconnect()

if __name__ == "__main__":
    asyncio.run(main())