import matplotlib.pyplot as plt
import pandas as pd
from cycler import cycler

"""
Plotter class to be used with client when processing and plotting BiT data.
"""
class Plotter:
	def __init__(self, time_array, level_array, fan_speed_array, custom_cycler=None):
		if custom_cycler is None:
			self.custom_cycler = cycler(color=['c', 'm', 'k'])
		else:
			self.custom_cycler = custom_cycler
		self.time_array = time_array
		self.level_array = level_array
		self.fan_speed_array = fan_speed_array

	"""
	Method to combine both subplots of data onto one display.
	"""
	def single_plot(self, pdf_path="./Data/bit_plot.pdf"):
		fs_lines, level_lines = [], []
		fig, ax1 = plt.subplots(figsize=(14, 8))

		fs_lines = ax1.plot(self.time_array, self.fan_speed_array, '.-')
		ax1.legend(fs_lines, ["Fan 4", "Fan 3", " Fan 2", " Fan 1"], bbox_to_anchor=(1.04, 1), loc="upper left")
		ax1.set_xlabel("Time (s)")
		ax1.set_ylabel("Fan Speed (rpm)")

		ax2 = ax1.twinx()
		ax2.set_prop_cycle(self.custom_cycler)
		level_lines = ax2.plot(self.time_array, self.level_array, '.--')
		ax2.legend(level_lines, ["Level 4", " Level 3", " Level 2"], bbox_to_anchor=(1.04, 0.75), loc="lower left")
		ax2.set_ylabel("Ball Level")

		fig.tight_layout()
		plt.savefig(pdf_path)
		plt.show()

	def data_to_csv(self, csv_path):
		# Exporting data to .csv file using pandas.
		fan_speed_df = pd.DataFrame(self.fan_speed_array)
		level_df = pd.DataFrame(self.level_array)
		time_df = pd.DataFrame(self.time_array)

		fan_speed_df.to_csv(csv_path, header=["Fan #4", "Fan #3", "Fan #2", "Fan #1"], index=False)
		level_df.to_csv(csv_path, mode='a', header=["Level #4", "Level #3", "Level #2"], index=False)
		time_df.to_csv(csv_path, float_format='%.1f', mode='a', header=["Time (s)"], index=False)