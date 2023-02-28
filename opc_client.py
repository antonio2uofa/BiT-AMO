import asyncio
import time
from client_classes import *
from asyncua import Client
from typing import List


# Define connectivity strings
URL = "opc.tcp://BB0253:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"

CSV_PATH = "./Data/bit_data.csv"
RGS_CSV = "./Data/rgs_signals.csv"
IMG_PATH = "./Data/Images/"

async def main():

    gain_reader = Reader(RGS_CSV)

    gain4, gain3, gain2, gain1 = [], [], [], []
    gain4, gain3, gain2, gain1 = gain_reader.get_fan_gains()

    fanspeed_array, level_array, time_array = [], [], []

    print(f"Connecting to {URL} ...")
    async with Client(url=URL) as client:
        # Find the namespace index
        ns_idx = await client.get_namespace_index(NAMESPACE)
        print(f"Namespace Index for '{NAMESPACE}': {ns_idx}")

        objects = client.nodes.objects
        print("Objects node is: ", objects)

        bit_obj = await objects.get_child(f"{ns_idx}:BIT Object")

        """
        Loop sets fanspeeds then checks the levels and fanspeeds at the same
        time. We get the time of each call and store those values for plotting.
        """

        start_time = time.time()
        for i in range(1, 100, 1):

            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 4, gain4[i])
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 3, gain3[i])
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 2, gain2[i])
            # await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 1, 100)

            fanspeed_array.append(await bit_obj.call_method(f"{ns_idx}:get_fanspeeds"))

            level_array.append([
                await bit_obj.call_method(f"{ns_idx}:get_level", 4),
                await bit_obj.call_method(f"{ns_idx}:get_level", 3),
                await bit_obj.call_method(f"{ns_idx}:get_level", 2),
            ])

            gain_reader.save_imgs(IMG_PATH)

            time_array.append(time.time() - start_time)

        plotter = Plotter(time_array, level_array, fanspeed_array)

        plotter.data_to_csv(CSV_PATH)
        plotter.single_plot()

if __name__ == "__main__":
    asyncio.run(main())