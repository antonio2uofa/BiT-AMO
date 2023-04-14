import asyncio
import time
from client_classes import *
from asyncua import Client
from antony_mpc import *
import optuna
import ast

# Define connectivity strings
URL = "opc.tcp://BB0253:4840/freeopcua/server/"
NAMESPACE = "http://examples.freeopcua.github.io"

CSV_PATH = "./Data/bit_data/bit_data_6.csv"
RGS_CSV = "./Data/MATLAB/rgs_signals_6.csv"
IMG_PATH = "./Data/Images/"

# OPT_DIC = {'a11': 8.924878438427847, 'b11': 0.1212626176705919, 'c11': 0.3044233591864853,
#     'a12': 0.3603578367964395, 'b12': 0.08587943006267727, 'c12': 0.1834277226838774,
#     'a13': 5.5849991410101625, 'b13': 0.05964899791987853, 'c13': 0.16871088993692984,
#     'a21': 4.796405529212242, 'b21': 0.263515089062357, 'c21': 0.10183895598624049,
#     'a22': 9.77991187241358, 'b22': 0.7982350979047457, 'c22': 0.01886048772391155,
#     'a23': 7.10197747764112, 'b23': 0.5121667284119515, 'c23': 0.07146080576477896,
#     'a31': 6.981128915956763, 'b31': 0.12163619132265063, 'c31': 0.14806989265279968,
#     'a32': 0.7127164788547135, 'b32': 0.8742644921022402, 'c32': 0.07337697917588437,
#     'a33': 9.883520903404438, 'b33': 0.2863680881403229, 'c33': 0.003604126553917189}

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

async def main():
    level_df = pd.read_csv("./Data/bit_data/bit_data_6_model.csv", header=None)
    my_arr = level_df.to_numpy()
    minmax_arr = [ast.literal_eval(my_arr[i][0]) for i in range(4)]

    # gain4, gain3, gain2, gain1 = ([] for i in range(4))
    # fanspeed_array, level_array, time_array, sampling_array, height_sp = ([] for i in range(5))
    # gain_reader = Reader(RGS_CSV)
    # gain4, gain3, gain2, gain1 = gain_reader.read_fan_gains()
    # gain_reader.read_frames(IMG_PATH)

    print(f"Connecting to {URL} ...")
    async with Client(url=URL) as client:
        ns_idx = await client.get_namespace_index(NAMESPACE)
        bit_obj = await client.nodes.objects.get_child(f"{ns_idx}:BIT Object")
        
        sampler = optuna.samplers.CmaEsSampler()
        study = optuna.create_study(direction='minimize', sampler=sampler)
        study.optimize(lambda trial: objective(trial, ns_idx, bit_obj, minmax_arr), n_trials=100)
        print(study.best_value)
        print(study.best_params)

        # calib_results = await calibrate(ns_idx, bit_obj, stall=4)
        # calib_results = np.round(calib_results, 0)
        # calib_pd = pd.DataFrame(calib_results)
        # calib_pd.to_csv('./Data/bit_data/calib_results.csv', index=False, header=False)
        # await bit_obj.call_method(f"{ns_idx}:reset_bit")
        # await asyncio.sleep(2)
        # opt_values = np.array(list(OPT_DIC.values()))
        # umax, umin, pred_horizon, num_tubes, num_variables = 1.0, 0.0, 2, 3, len(opt_values)
        # num_rows = int(num_variables / num_tubes)
        # mat_values = np.reshape(opt_values, (num_rows, num_tubes))
        # Q, R1, R2 = (np.reshape(mat_values[: , i], (3,3)) for i in range(num_tubes))
        # umax, umin, pred_horizon, num_tubes, num_variables = 1.0, 0.0, 2, 3
        # P = 'none'
        # sps = np.array([0.7 , 0.4, 0.6 , 0.3])
        # sp_index = 0
        # height_sp.append(np.tile(sps[sp_index], num_tubes)
        # uk = np.array([0.5, 0.5, 0.5])
        # controller = MPC(num_tubes=3, pred_horizon=3)
        # """
        # Loop sets fanspeeds then checks the levels and fanspeeds at the same
        # time. We get the time of each call and store those values for plotting.
        # """
        # for i in range(len(gain1)):
        #     sample_start = time.time()
            # speed, levels = await sample(ns_idx, bit_obj, uk[0], uk[1], uk[2], 1.0, normalized=True)
            # speed, levels = await sample(ns_idx, bit_obj, gain4[i], gain3[i], gain2[i], 100, normalized=False)
            # xk, norm_speeds = await norm(calib_results, levels, speed[0:3])
            # uk, _ = controller.nl_mpc(Q, R1, R2, xk, pred_horizon, umin, umax, xk_sp=height_sp[i], P=P)
            # height_sp.append(np.tile(sps[sp_index], num_tubes))

            # my_tuple = await asyncio.gather(
            # sample(ns_idx, bit_obj, gain4[i], gain3[i], gain2[i], 100),
            # asyncio.to_thread(gain_reader.read_frames, IMG_PATH),
            # )
            # fanspeed_array.append(my_tuple[0][0])
            # level_array.append(my_tuple[0][1])

        #     fanspeed_array.append(speed)
        #     level_array.append(levels)
            
        #     delay = 0.5 - (time.time() - sample_start)
        #     if(delay > 0):
        #         time.sleep(delay)
        #     sampling_array.append(time.time() - sample_start)
        
        # time_array = np.round(np.array(sampling_array), 1)
        # time_array = np.cumsum(time_array)

            # # Set point change
            # if i > 0 and i % 100 == 0:  # set point change frequency (units: samples)
            #     sp_index += 1
            #     if sp_index > len(sps) - 1:  # loop around set point array if its end is reached
            #         sp_index = 0
        

        # height_sp.pop(0)
        # plotter = Plotter(sampling_array, time_array, level_array, fanspeed_array, height_sp)
        # plotter.data_to_csv("./Data/bit_data/bit_data_6.csv")
        # plotter.double_plot("./Data/bit_data/bit_plot_6.pdf")

        # del gain_reader

if __name__ == "__main__":
    asyncio.run(main())