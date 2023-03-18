import pandas as pd
import numpy as np
import pysindy as ps
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

def main():
    gain_df = pd.read_csv('./Data/bit_data_1.csv')
    data_matrix = gain_df.to_numpy()

    U, Y = data_matrix[:, 0:3], data_matrix[:, 4:7]
    U_train, U_test = U[0:2879], U[2880:-1]
    Y_train, Y_train_t1, Y_test, Y_test_t1 = Y[0:2879], Y[1:2880], Y[2880:-1], Y[2881:]

    training_data = np.concatenate((U_train, Y_train, Y_train_t1), axis=1)
    training_data -= np.mean(training_data, axis=0)
    testing_data = np.concatenate((U_test, Y_test, Y_test_t1), axis=1)
    testing_data -= np.mean(testing_data, axis=0)

    feature_library = ps.PolynomialLibrary(degree=3)
    optimizer = ps.STLSQ(threshold=0.3)
    feature_names = ['u4','u3','u2','y4','y3','y2','y4_t1','y3_t1','y2_t1']

    model = ps.SINDy(feature_names=feature_names,
    feature_library=feature_library,
    optimizer=optimizer)

    model.fit(training_data, t=0.5)
    model.print()
    results = model.predict(testing_data)
    fig, axs = plt.subplots(2, sharex='all', figsize=(12, 7))  # OD
    fig.suptitle("Actual vs Predicted Results")
    fs_lines = axs[0].plot(results, ls='-.', label='predicted')
    level_lines = axs[1].plot(testing_data, ls='--', label='actual')
    mse = mean_squared_error(testing_data, results)
    rs = r2_score(testing_data, results)
    axs[0].legend()
    axs[1].legend()
    print(mse)
    print(rs)
    plt.show()
if __name__ == '__main__':
    main()