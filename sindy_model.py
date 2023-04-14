import pandas as pd
import numpy as np
import pysindy as ps
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing

NUM_TUBES = 3

def main():
    minmax_df = pd.read_csv('./Data/bit_data/calib_results.csv', header=None)
    level_df = pd.read_csv('./Data/bit_data/bit_data_6.csv')
    gain_df = pd.read_csv('./Data/MATLAB/rgs_signals_6.csv')

    minmax_array, data_array, gain_array = minmax_df.to_numpy(), level_df.to_numpy()[3:, :], gain_df.to_numpy()[3:, :]
    
    # _, _, max_lvl, min_lvl = minmax_array
    # tube_height = 100
    # # Scale height to cm
    # height_consts = tube_height / (max_lvl - min_lvl)
    # curr_heights = height_consts * (max_lvl - Y)
    # Y = np.round(curr_heights, 0)

    gain_scaler = preprocessing.MinMaxScaler()
    height_scaler = preprocessing.MinMaxScaler()

    Y = height_scaler.fit_transform(data_array[:, 4:7])
    gain_scaler.fit_transform(gain_array[:, 0:3])

    minmax_vals = np.concatenate((height_scaler.data_min_, height_scaler.data_max_,
                                gain_scaler.data_min_, gain_scaler.data_max_), axis=0)
    num_elements = int(minmax_vals.size / NUM_TUBES)
    minmax_vals = np.reshape(minmax_vals, (num_elements, NUM_TUBES))

    for i in range(num_elements):
        print(list(minmax_vals[i]))
    
    U = gain_scaler.fit_transform(data_array[:, 0:3])

    train_split = round(0.8 * data_array.shape[0])
    test_split = data_array.shape[0] - train_split

    U_train, U_test = U[0:train_split], U[train_split:]
    Y_train, Y_test = Y[0:train_split], Y[train_split:]

    feature_library = ps.PolynomialLibrary(degree=3)
    optimizer = ps.STLSQ(threshold=0.13)
    diff_method = ps.SmoothedFiniteDifference()
    feature_names = ['x4','x3','x2','u4','u3','u2']

    model = ps.SINDy(discrete_time=True,
    differentiation_method=diff_method,
    feature_names=feature_names,
    feature_library=feature_library,
    optimizer=optimizer)

    model.fit(x=Y_train, u=U_train, t=0.5, unbias=True)
    model.print()

    results = model.simulate(Y_test[0, 0:3], test_split, U_test)

    fig, axs = plt.subplots(3, sharex='all', figsize=(12, 7))  # OD
    fig.suptitle("Predicted vs Actual Results")
    
    count = 4
    for i in range(3):
        axs[i].plot(results[:, i], color='tab:blue', ls='--', label=f'Tube {i+count} predicted')
        axs[i].plot(Y_test[:, i], color='tab:gray', alpha=0.5, label=f'Tube {i+count} actual')
        axs[i].legend(loc='upper left')
        count -= 2

    mse = round(mean_squared_error(Y_test, results), 5)
    rs = round(r2_score(Y_test, results), 5)
    axs[0].title.set_text(f'RSquare: {rs} MSE: {mse}')
    plt.show()

if __name__ == '__main__':
    main()
