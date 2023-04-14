from opcua import ua, uamethod, Server
import bit_functions as bit 
from server_classes import FanSpeedWrapper
import time

# Global variables
ENDPOINT = "opc.tcp://BB0253:4840/freeopcua/server/"
SERVER_NAME = "Antonio OPC-UA Server"
URI = "http://examples.freeopcua.github.io"
_WRAPPER = FanSpeedWrapper()

@uamethod
def set_fanspeeds(parent, fan_4: int, fan_3: int, fan_2: int, fan_1: int, normalized):
	bit.set_fanspeeds(fan_4, fan_3, fan_2, fan_1, normalized)

@uamethod
def set_fanspeed(parent, tube_num: int, level: int):
	bit.set_fanspeed(tube_num, level)

@uamethod
def get_level(parent, tube_num: int):
   return bit.get_level(tube_num)

@uamethod
def get_fanspeeds(parent):
	return _WRAPPER.get_fanspeeds()

@uamethod
def reset_bit(parent):
	_WRAPPER.reset_bit()

def main():
	# Load into memory functions from bit
	_WRAPPER.setup_bit()

	# Start server
	server = Server()
	server.set_endpoint(ENDPOINT)
	server.set_server_name(SERVER_NAME)
	
	idx = server.register_namespace(URI)
	myobj = server.nodes.objects.add_object(idx, "BIT Object")
	
	myobj.add_method(idx, "set_fanspeeds", set_fanspeeds, [ua.VariantType.Int32,
	ua.VariantType.Int32, ua.VariantType.Int32, ua.VariantType.Int32, ua.VariantType.Boolean], [])
	myobj.add_method(idx, "set_fanspeed", set_fanspeed, [ua.VariantType.Int32, ua.VariantType.Int32], [])
	myobj.add_method(idx, "get_level", get_level, [ua.VariantType.Int32], [ua.VariantType.Int32])
	myobj.add_method(idx, "get_fanspeeds", get_fanspeeds, [], [ua.VariantType.Int32])
	myobj.add_method(idx, "reset_bit", reset_bit, [], [])

	server.start()

	try:
		while(True):
			time.sleep(0.01)

	finally:
		server.stop()

if __name__=="__main__":
	main()