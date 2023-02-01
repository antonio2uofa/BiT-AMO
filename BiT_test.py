from BiT_functions import *

def main():
	init_bit()
	set_fanspeed(3, 0)
	set_fanspeed(2, 0)
	set_fanspeed(4, 0)
	for i in range(7):
		print(get_level(4))
		print(get_level(2))
		print(get_level(3))

if __name__ == '__main__':
	main()