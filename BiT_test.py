from bit_functions import *
import matplotlib.pyplot as plt
from client_classes import *
import numpy as np
import time

def main():

	fanspeed_array, level_array, time_array = [], [], []
	count = 0
	start = time.time()
	while count < 10:
		fanspeed_array.append(np.random.rand(1,4).tolist()[0])
		level_array.append(np.random.rand(1,3).tolist()[0])
		time_array.append(time.time()-start)
		time.sleep(0.1)
		count += 1

	plotter = Plotter(time_array, level_array, fanspeed_array)
	plotter.single_plot()
	plotter.data_to_csv("./testing.csv")


if __name__ == '__main__':
	main()