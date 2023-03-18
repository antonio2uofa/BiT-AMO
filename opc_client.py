import asyncio
import time
from client_classes import *
from asyncua import Client

# Define connectivity strings
URL = "opc.tcp://BB0253:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"

CSV_PATH = "./Data/bit_data_2.csv"
RGS_CSV = "./Data/rgs_signals.csv"
IMG_PATH = "./Data/Images/"

async def set_fanspeeds():
    

async def main():

    gain4, gain3, gain2, gain1 = [], [], [], []
    fanspeed_array, level_array, time_array, sampling_array = [], [], [], []

    gain_reader = Reader(RGS_CSV)
    gain4, gain3, gain2, gain1 = gain_reader.read_fan_gains()
    loop = asyncio.get_running_loop()

    print(f"Connecting to {URL} ...")
    async with Client(url=URL) as client:
        ns_idx = await client.get_namespace_index(NAMESPACE)
        bit_obj = await client.nodes.objects.get_child(f"{ns_idx}:BIT Object")

        await bit_obj.call_method(f"{ns_idx}:reset_bit")
        time.sleep(2)

        """
        Loop sets fanspeeds then checks the levels and fanspeeds at the same
        time. We get the time of each call and store those values for plotting.
        """

        loop_start = time.time()
        for i in range(len(gain4)):
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 4, gain4[i])
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 3, gain3[i])
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 2, gain2[i])

            sampling_start = time.time()
            fanspeed_array.append(await bit_obj.call_method(f"{ns_idx}:get_fanspeeds"))
           
            level_array.append([
                await bit_obj.call_method(f"{ns_idx}:get_level", 4),
                await bit_obj.call_method(f"{ns_idx}:get_level", 3),
                await bit_obj.call_method(f"{ns_idx}:get_level", 2),
            ])
            sampling_array.append(time.time() - sampling_start)

            time_array.append(time.time() - loop_start)

        plotter = Plotter(sampling_array, time_array, level_array, fanspeed_array)
        plotter.data_to_csv(CSV_PATH)
        plotter.double_plot()

        del gain_reader

if __name__ == "__main__":
    asyncio.run(main())