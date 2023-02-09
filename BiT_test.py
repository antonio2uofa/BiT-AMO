from BiT_functions import *
import multiprocessing as mp
import matplotlib.pyplot as plt  
import time

def mp_get_fanspeeds(process_queue):
	process_queue.put(get_fanspeeds())

def main():

	processes, fanspeed_array, level_array, time_array = [], [], [], []
	process_queue = mp.Queue()

	init_bit()
	start_time = time.time()

	for i in range(0, 102, 2):
		set_fanspeed(3, i)
		set_fanspeed(2, i)
		set_fanspeed(4, i)

		level_array.append([
                get_level(2),
                get_level(3),
                get_level(4),
            ])

		process = mp.Process(target=mp_get_fanspeeds, args=(process_queue,))
		processes.append(process)
		process.start()

		loop_time = time.time()

		time_array.append(loop_time-start_time)
		time.sleep(0.5)


	for process in processes:
		process.join()

	while not process_queue.empty():
		fanspeed_array.append(process_queue.get())

	x = time_array
	y1 = level_array
	y2 = fanspeed_array

	plt.plot(x, y1, '-o', x, y2, '-o')
	plt.show()

if __name__ == '__main__':
	main()