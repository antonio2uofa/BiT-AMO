import asyncio
from asyncua import Client, Node, ua

import pandas as pd
import time
import multiprocessing as mp
import matplotlib.pyplot as plt  

# Define connectivity strings
URL = "opc.tcp://142.244.38.72:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"
CSV_PATH = r"C:\Users\OPCUSER\AppData\Local\Programs\Python\Python38-32\BiT-AMO\Data\bit_data.csv"

async def main():

    fanspeed_array, level_array, time_array = [], [], []
    fan_factor = -1

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
        while(fan_factor < 100):
            fan_factor += 1
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 1, fan_factor)
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 2, fan_factor)
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 3, fan_factor)
            await bit_obj.call_method(f"{ns_idx}:set_fanspeed", 4, fan_factor)

            fanspeed_array.append(await bit_obj.call_method(f"{ns_idx}:get_fan_speeds"))

            level_array.append([
                await bit_obj.call_method(f"{ns_idx}:get_level", 2),
                await bit_obj.call_method(f"{ns_idx}:get_level", 3),
                await bit_obj.call_method(f"{ns_idx}:get_level", 4),
                ])

            loop_time = time.time()
            time_array.append(loop_time-start_time)

        
        # Exporting data to .csv file using pandas.
        fanspeed_df = pd.DataFrame(fanspeed_array)
        level_df = pd.DataFrame(level_array)
        time_df = pd.DataFrame(time_array)

        fanspeed_df.to_csv(CSV_PATH, header=["Fan #1", "Fan #2", "Fan #3", "Fan #4"], index=False)
        level_df.to_csv(CSV_PATH, mode='a', header=["Level #2", "Level #3", "Level #4"], index=False)
        time_df.to_csv(CSV_PATH, float_format='%.1f', mode='a', header=["Time (s)"], index=False)

        # Plotting information
        x = time_array
        y1 = level_array
        y2 = fanspeed_array

        plt.plot(x, y1, '-o', x, y2, '-o')
        plt.show()

if __name__ == "__main__":
    asyncio.run(main())