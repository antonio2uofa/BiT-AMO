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
	
	Q_factor = trial.suggest_float('Q_factor', 0.0, 10.0)
	R1_factor = trial.suggest_float('R1_factor', 0.0, 10.0)
	R2_factor = trial.suggest_float('R2_factor', 0.0, 10.0)

	Q_matrix = np.eye(3) * Q_factor
	R1_matrix, R2_matrix = np.eye(3) * R1_factor, np.eye(3) * R2_factor
	sample_num=200
	error = score.get_score(minmax_arr, sample_num, Q_matrix, R1_matrix, R2_matrix)
	print(f'Trial {trial.number} - Q_factor: {Q_factor}, R1_factor: {R1_factor}, R2_factor: {R2_factor}. Error: {error}')
	return error

def main():
	level_df = pd.read_csv("./Data/bit_data/bit_data_6_model.csv", header=None)
	my_arr = level_df.to_numpy()
	minmax_arr = [ast.literal_eval(my_arr[i][0]) for i in range(4)]

	client = Client(URL)
	try:
		client.connect()
		ns_idx = client.get_namespace_index(NAMESPACE)
		bit_obj = client.nodes.objects.get_child(f"{ns_idx}:BIT Object")
		sample(ns_idx, bit_obj, 100, 100, 100, 100, normalized=False, stall=0)
		
		# calibrated_matr = calibrate(stall=3)
		# minmax_arr[0:2] = [calibrated_matr[2].tolist(), calibrated_matr[3].tolist()]
		# print(minmax_arr)

		# sampler = optuna.samplers.TPESampler()
		# # sampler = optuna.samplers.CmaEsSampler()
		# study = optuna.create_study(direction='minimize', sampler=sampler, pruner=optuna.pruners.HyperbandPruner())
		# study.enqueue_trial({'Q_factor': 9.549320469964073, 'R1_factor': 1.8358664780687504, 'R2_factor': 0.8400727361706875})
		# study.enqueue_trial({'Q_factor': 9.992497706534994, 'R1_factor': 1.9556211584901746, 'R2_factor': 0.8999830237389322})
		# study.optimize(lambda trial: objective(trial, ns_idx, bit_obj, minmax_arr), n_trials=800)
		# print(study.best_value)
		# print(study.best_params)

	finally:
		client.disconnect()

if __name__ == '__main__':
	main()