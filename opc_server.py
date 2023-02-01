import asyncio

from asyncua import Server, ua
from asyncua.common.methods import uamethod

from BiT_functions import *

async def main():
    # setup our server
    server = Server()

    # wait until server starts
    await server.init()

    # bind the server to an IP
    server.set_endpoint("opc.tcp://142.244.38.72:4840/freeopcua/server/")

    server.set_server_name("Free Example Server")

    security_array = [ua.SecurityPolicyType.NoSecurity, ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt, ua.SecurityPolicyType.Basic256Sha256_Sign]

    server.set_security_policy(security_array)

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "BIT Object")
    myvar = await myobj.add_variable(idx, "Level 1", get_level(1))
    myvar2 = await myobj.add_variable(idx, "Level 2", get_level(2))
    myvar3 = await myobj.add_variable(idx, "Level 3", get_level(3))
    myvar4 = await myobj.add_variable(idx, "Level 4", get_level(4))
    
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    await myvar2.set_writable()
    await myvar3.set_writable()
    await myvar4.set_writable()

    async with server:
        while True:
            await asyncio.sleep(1)

            await myvar.write_value(get_level(1))
            await myvar2.write_value(get_level(2))
            await myvar3.write_value(get_level(3))
            await myvar4.write_value(get_level(4))


if __name__ == "__main__":
    asyncio.run(main())