from opcua import Client
from client_classes import *
from antony_mpc import *
import optuna
import ast

# Define connectivity strings
URL = "opc.tcp://BB0253:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"

CSV_PATH = "./Data/bit_data/bit_data_6.csv"
RGS_CSV = "./Data/MATLAB/rgs_signals_6.csv"
IMG_PATH = "./Data/Images/"

def objective(trial, ns_idx, bit_obj, minmax_arr):
	score = MPC(ns_idx, bit_obj, num_tubes=3, pred_horizon=2)
	Q_matrix, R1_matrix, R2_matrix = (np.zeros((3, 3)) for i in range(3))
	for i in range(3):
		for j in range(3):
			Q_matrix[i][j] = trial.suggest_float(f'a{i+1}{j+1}', 0.0, 10.0)
			R1_matrix[i][j] = trial.suggest_float(f'b{i+1}{j+1}', 0.0, 10.0)
			R2_matrix[i][j] = trial.suggest_float(f'c{i+1}{j+1}', 0.0, 10.0)
			
	return score.get_score(minmax_arr, sample_num=400,Q=np.array(Q_matrix),
							R1=np.array(R1_matrix), R2=np.array(R2_matrix))

def main():
	level_df = pd.read_csv("./Data/bit_data/bit_data_6_model.csv", header=None)
	my_arr = level_df.to_numpy()
	minmax_arr = [ast.literal_eval(my_arr[i][0]) for i in range(4)]

	client = Client(URL)
	try:
		client.connect()
		ns_idx = client.get_namespace_index(NAMESPACE)
		bit_obj = client.nodes.objects.get_child(f"{ns_idx}:BIT Object")

		sampler = optuna.samplers.CmaEsSampler()
		study = optuna.create_study(direction='minimize', sampler=sampler)
		study.optimize(lambda trial: objective(trial, ns_idx, bit_obj, minmax_arr), n_trials=100)
		print(study.best_value)
		print(study.best_params)

	finally:
		client.disconnect()

if __name__ == '__main__':
	main()