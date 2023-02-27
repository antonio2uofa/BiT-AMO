import asyncio
import bit_functions as bit 
from server_classes import FanSpeedWrapper

from asyncua import Server, ua
from asyncua.common.methods import uamethod

# Global variables
ENDPOINT = "opc.tcp://BB0253:4840/freeopcua/server/"
SERVER_NAME = "Antonio OPC-UA Server"
URI = "http://examples.freeopcua.github.io"
_WRAPPER = FanSpeedWrapper()

@uamethod
def set_fanspeed(parent, tube_num: int, level: int):
    bit.set_fanspeed(tube_num, level)

@uamethod
def get_level(parent, tube_num: int):
   return bit.get_level(tube_num)

@uamethod
def get_fanspeeds(parent):
    return _WRAPPER.get_fanspeeds()

async def main():
	# Load into memory functions from bit
    _WRAPPER.setup_bit()

    # Start server
    server = Server()
    await server.init()

    # bind the server to an IP
    server.set_endpoint(ENDPOINT)
    server.set_server_name(SERVER_NAME)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    idx = await server.register_namespace(URI)
    myobj = await server.nodes.objects.add_object(idx, "BIT Object")

    # Adding methods to our object in OPC-UA
    await myobj.add_method(idx, "set_fanspeed", set_fanspeed, [ua.VariantType.Int32, ua.VariantType.Int32], [])
    await myobj.add_method(idx, "get_level", get_level, [ua.VariantType.Int32], [ua.VariantType.Int32])
    await myobj.add_method(idx, "get_fanspeeds", get_fanspeeds, [], [ua.VariantType.Int32])

    # Adding variables that represent the ball levels
    #level_1 = await myobj.add_variable(idx, "Level 1", get_level(1))
    #level_2 = await myobj.add_variable(idx, "Level 2", get_level(2))
    #level_3 = await myobj.add_variable(idx, "Level 3", get_level(3))
    #level_4 = await myobj.add_variable(idx, "Level 4", get_level(4))
    
    # Set variables to be writable by clients
    #await level_1.set_writable()
    #await level_2.set_writable()
    #await level_3.set_writable()
    #await level_4.set_writable()

    async with server:
        while True:
            await asyncio.sleep(0.1)
    """
    Goal was to use this loop to constantly update values.
    However, it interferes with the client calling the methods
    implemented above since only one program can communicate
    with the Rt-DAC USB at a time.
    """
    #        await level_1.write_value(bit.get_level(1))
    #        await level_2.write_value(bit.get_level(2))
    #        await level_3.write_value(bit.get_level(3))
    #        await level_4.write_value(bit.get_level(4))


if __name__ == "__main__":
    asyncio.run(main())