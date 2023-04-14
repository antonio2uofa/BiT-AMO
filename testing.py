import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
import ast

level_df = pd.read_csv("./Data/bit_data/bit_data_6_model.csv", header=None)
my_arr = level_df.to_numpy()
my_arr = [ast.literal_eval(my_arr[i][0]) for i in range(4)]
my_arr = [1, 2, 3]
my_2_arr = [4, 5, 6]

# gain_df = pd.read_csv('./Data/MATLAB/rgs_signals_5.csv')

# level_array = level_df.to_numpy()[2:, :]
# gain_array = gain_df.to_numpy()[2:, :]

# level_scaler = preprocessing.MinMaxScaler()
# gain_scaler = preprocessing.MinMaxScaler()

# U = level_scaler.fit_transform(level_array)

# time_array = U[:, 7]

# gain_func_df = pd.read_csv('./Data/MATLAB/rgs_signals_5.csv')
# data_matrix = gain_func_df.to_numpy()
# Y = data_matrix[:, 0:3]

# Y = np.zeros((2010, 3))
# count = 0
# for _ in range(10):
#     for i in range(99,-1,-1):
#         Y[count] = [i, i, i]
#         count += 1
#     for i in range(101):
#         Y[count] = [i , i, i]
#         count += 1
# Y = gain_scaler.fit_transform(gain_array)
# sorted_array = np.argsort(U[:, 0:3], axis=0)

# fig, ax = plt.subplots(3,3, figsize=(10, 7), sharex='all', constrained_layout=True)

# mse4, mse3, mse2 = (round(mean_squared_error(U[:,i], Y[:,i]), 5) for i in range(3))

# ax[0,0].plot(time_array, U[:,0], '-.', color='tab:blue', alpha=0.5, label='Tube 4')
# ax[1,0].plot(time_array, Y[:,0], '-', color='tab:red', alpha=0.5, label='Tube 4')
# ax[2,0].plot(time_array, Y[:,0], '-', color='tab:red', alpha=0.5)
# ax[2,0].plot(time_array, U[:,0], '-.', color='tab:blue', alpha=0.5)
# ax[0,0].legend()
# ax[1,0].legend()

# ax[0,1].plot(time_array, U[:,1], '-.', color='tab:blue', alpha=0.5, label='Tube 3')
# ax[1,1].plot(time_array, Y[:,1], '-', color='tab:red', alpha=0.5, label='Tube 3')
# ax[2,1].plot(time_array, Y[:,1], '-', color='tab:red', alpha=0.5)
# ax[2,1].plot(time_array, U[:,1], '-.', color='tab:blue', alpha=0.5)
# ax[0,1].legend()
# ax[1,1].legend()

# ax[0,2].plot(time_array, U[:,2], '-.', color='tab:blue', alpha=0.5, label='Tube 2')
# ax[1,2].plot(time_array, Y[:,2], '-', color='tab:red', alpha=0.5, label='Tube 2')
# ax[2,2].plot(time_array, Y[:,2], '-', color='tab:red', alpha=0.5)
# ax[2,2].plot(time_array, U[:,2], '-.', color='tab:blue', alpha=0.5)
# ax[0,2].legend()
# ax[1,2].legend()
# ax[0,1].set_title(f'RPM')
# ax[1,1].set_title(f'Fan Speed Factor')
# ax[2,0].set_title(f'MSE 4: {mse4}')
# ax[2,1].set_title(f'MSE 3: {mse3}')
# ax[2,2].set_title(f'MSE 2: {mse2}')

# plt.tight_layout()
# plt.show()

# coefficients = np.polyfit(U[:, 0], Y[:, 0], 1)

# x = np.linspace(0, 100, 101)
# y = coefficients[0] * x + coefficients[1]

# plt.plot(U[:, 0], Y[:, 0], 'b-')
# plt.plot(x, y, 'r--')

# feature_library = ps.PolynomialLibrary(degree=3)
# optimizer = ps.STLSQ(threshold=0.001)
# diff_method = ps.SmoothedFiniteDifference()
# feature_names = ['x4','x3','x2','u4','u3','u2']

# model = ps.SINDy(discrete_time=True,
# differentiation_method=diff_method,
# feature_names=feature_names,
# feature_library=feature_library,
# optimizer=optimizer)

# model.fit(x=Y, u=U, t=0.5, unbias=True)
# model.print()
