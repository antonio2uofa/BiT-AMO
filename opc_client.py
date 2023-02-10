import asyncio
import time
from client_classes import *
from asyncua import Client, ua


# Define connectivity strings
URL = "opc.tcp://142.244.38.72:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"
CSV_PATH = "./Data/bit_data.csv"

async def main():

    fan_speed_array, level_array, time_array, voltage_array = [], [], [], []

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

        count = 0;
        await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 1, 100)
        await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 2, 60)
        await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 3, 70)
        await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 4, 55)

        start_time = time.time()
        while(count < 10):
            count += 1
            fan_speed_array.append(await bit_obj.call_method(f"{ns_idx}:get_fan_speeds"))

            level_array.append([
                await bit_obj.call_method(f"{ns_idx}:get_level", 4),
                await bit_obj.call_method(f"{ns_idx}:get_level", 3),
                await bit_obj.call_method(f"{ns_idx}:get_level", 2),
                ])

            loop_time = time.time()
            time_array.append(loop_time-start_time)

        plotter = Plotter(time_array, level_array, fan_speed_array)
        plotter.data_to_csv(CSV_PATH)
        plotter.single_plot()

if __name__ == "__main__":
    asyncio.run(main())