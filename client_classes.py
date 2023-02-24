import matplotlib.pyplot as plt
import pandas as pd
from cycler import cycler

"""
Plotter class to be used with client when processing and plotting BiT data.
"""
class Plotter:
	def __init__(self, time_array, level_array, fanspeed_array, custom_cycler=None):
		if custom_cycler is None:
			self.custom_cycler = cycler(color=['c', 'm', 'k'])
		else:
			self.custom_cycler = custom_cycler

		self.time_array = time_array
		self.level_array = level_array
		self.fanspeed_array = fanspeed_array

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
		fanspeed_df = pd.DataFrame(self.fanspeed_array)
		level_df = pd.DataFrame(self.level_array)
		time_df = pd.DataFrame(self.time_array)

		fanspeed_df.to_csv(csv_path, header=["Fan #4", "Fan #3", "Fan #2", "Fan #1"], index=False)
		level_df.to_csv(csv_path, mode='a', header=["Level #4", "Level #3", "Level #2"], index=False)
		time_df.to_csv(csv_path, float_format='%.1f', mode='a', header=["Time (s)"], index=False)

class Reader:
	def __init__(self, csv_path):
		self.csv_path = csv_path
		self.fan_gain_df = pd.read_csv(csv_path)

	def get_fan_gains(self):
		headers = list(self.fan_gain_df.columns.values)

		tube4_gains = self.fan_gain_df[f"{headers[0]}"].to_list()
		tube3_gains = self.fan_gain_df[f"{headers[1]}"].to_list()
		tube2_gains = self.fan_gain_df[f"{headers[2]}"].to_list()
		tube1_gains = self.fan_gain_df[f"{headers[3]}"].to_list()

		return tube4_gains, tube3_gains, tube2_gains, tube1_gains