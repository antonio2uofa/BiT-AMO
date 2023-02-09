import nidaqmx
#import matplotlib.pyplot as plt
#from collections import deque
import time

#def main():
	#queue = deque(maxlen = 10)

with nidaqmx.Task() as task:
	task.ai_channels.add_ai_voltage_chan("Dev1/ai0:3")
	print(task.read())
		# Commented Out Code is for reading/plotting voltage data
		#while True:
			#start = time.time()
			#queue.append(task.read())
			#task.read()
			#end = time.time()
			#print(end-start)
			# PLOTTING THE POINTS
			#plt.plot(queue)

			# SET Y AXIS RANGE
			#plt.ylim(-1,6)
			#
			# DRAW, PAUSE AND CLEAR
			#plt.draw()
			#plt.pause(0.005)
			#plt.clf()

#if __name__ == '__main__':
	#main()