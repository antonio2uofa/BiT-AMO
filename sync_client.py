from opcua import ua, Client

# Define connectivity strings
URL = "opc.tcp://BB0253:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"

def main():

	client = Client(URL)

	try:
		client.connect()
		ns_idx = client.get_namespace_index(NAMESPACE)
		bit_obj = client.nodes.objects.get_child(f"{ns_idx}:BIT Object")

		print(bit_obj.call_method(f"{ns_idx}:get_level", 4))

	finally:
		client.disconnect()

if __name__ == '__main__':
	main()