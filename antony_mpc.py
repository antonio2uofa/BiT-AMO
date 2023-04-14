from scipy.optimize import minimize
from client_classes import sample
import numpy as np

"""
Wrapper class for functions used to implement MPC Controller.
"""
class MPC:
    def __init__(self, ns_idx, bit_obj, num_tubes=3, pred_horizon=2):
        self.num_tubes = num_tubes
        self.pred_horizon = pred_horizon
        self.ns_idx = ns_idx
        self.bit_obj = bit_obj

    def nl_system_model(self, xk, uk):
        """MIMO nonlinear model of system"""
        x4, x3, x2 = xk
        u4, u3, u2 = uk

        x4_next = 0.263 + 0.775 * x4 + -0.642 * u4 + -0.110 * x4 * u4 + \
        0.465 * x4 * u3 + 0.915 * u4**2 + -0.298 * u4 * u3 + 0.540 * x4**2 * u4 + \
        -0.393 * x4**2 * u3 + -0.379 * x4 * u4**2 + -0.488 * u4**3 + 0.254 * u4**2 * u3

        x3_next = 0.796 + 1.039 * x3 + -3.447 * u3 + -0.190 * x3**2 + 0.665 * x3 * u3 + \
        4.665 * u3**2 + -0.724 * x3**3 + 2.436 * x3**2 * u3 + -2.759 * x3 * u3**2 + -1.945 * u3**3

        x2_next = 0.228 + 1.299 * x2 + -0.341 * u2 + -1.443 * x2**2 + 1.087 * x2**3

        x_next = np.array([x4_next, x3_next, x2_next])
        y_next = x_next
        
        return x_next, y_next

    def nl_mpc(self, Q, R1, R2, xk, N, umin, umax, xk_sp, P='none'):
        """ Determines optimal controller action using the set point error and model prediction """
        u_init = 50 * np.ones(self.num_tubes * N)
        u_bounds = ((umin, umax), (umin, umax), (umin, umax)) * N  # bounds on the input trajectory
        sol = minimize(self.nl_mpc_obj, u_init, args=(Q, R1, R2, P, xk, N, xk_sp), method='SLSQP', bounds=u_bounds,
                    options={'eps': 1e-6, 'disp': False})
        # the optimized input trajectory is stored in sol.x
        U = sol.x
        U = np.split(U, N)
        # only the first input value is implemented according to receding horizon implementation
        uk = U[0]

        return uk, sol.fun

    def nl_mpc_obj(self, U, Q, R1, R2, P, xk, N, xk_sp):
        """ Calculates cost function for SISO NONLINEAR MPC """
        ukprev = np.zeros(self.num_tubes)
        J = (xk - xk_sp) @ Q @ (xk - xk_sp)
        U = np.split(U, N)
        for k in range(0, N):
            # *OR put cost on CHANGE in controller output (added velocity term)
            uk = U[k]  # this U is the optimized input trajectory by 'minimize' used in mpc function
            du = uk - ukprev
            ukprev = uk
            xk, _ = self.nl_system_model(xk, uk)
            J += 0.5 * (xk - xk_sp) @ Q @ (xk - xk_sp) + 0.4 * uk @ R1 @ uk + 0.1 * du @ R2 @ du

        # Terminal cost term (is ignored if 'P' is a string)
        if type(P) != str:
            J += 0.5 * (xk - xk_sp) @ P @ (xk - xk_sp) - 0.5 * (xk - xk_sp) @ Q @ (xk - xk_sp)
        return J

    def get_score(self, minmax_arr, sample_num=400, Q=None, R1=None, R2=None):
        self.sample_num = sample_num
        self.fan_spd_factor, self.experiment_height, self.height_sp = (
        [np.array([0.0, 0.0, 0.0]) for i in range(self.sample_num+1)] for y in range(3))
        level_minmax = np.array(minmax_arr[0:2])
        gain_minmax = np.array(minmax_arr[2:])

        # Coefficients in cost function J (choose how much to penalize high error or high controller /
        # change-in controller output)
        P = 'none'

        # Lower and upper limits of controller (used in optimizer)
        umax = 1.0
        umin = 0.0

        # Create set point array
        sps = np.array([0.7 , 0.4, 0.6 , 0.3])
        sp_index = 0
        self.height_sp[0] = np.tile(sps[sp_index], self.num_tubes)
        self.experiment_height[0] = np.array([0.0, 0.0, 0.0])

        # Initial state of system
        uk, _ = self.nl_mpc(Q, R1, R2, self.experiment_height[0], self.pred_horizon, umin, umax, xk_sp=self.height_sp[0])
        self.fan_spd_factor[0] = np.round(uk, 0)

        # Run MPC algorithm for "sample number" of iterations
        for i in range(1, self.sample_num + 1):
            # print(f"===== Sample: {i}/{self.sample_num} =====")
            # self.time_array[i] = round(i * self.sample_time, 1)

            # Get current height
            uk = self.denormalize(gain_minmax, uk)
            speed, self.experiment_height[i] = sample(self.ns_idx, self.bit_obj, uk[0], uk[1], uk[2], 100, normalized=False)

            # Set point assignment
            self.height_sp[i] = np.tile(sps[sp_index], self.num_tubes)

            # Calculate optimal controller output (fan speed factors)
            uk, self.cost[i] = self.nl_mpc(Q, R1, R2, self.experiment_height[i], self.pred_horizon, umin, umax, xk_sp=self.height_sp[i], P=P)
            self.fan_spd_factor[i] = np.round(uk, 0)

            # Set point change
            if i > 0 and i % 100 == 0:  # set point change frequency (units: samples)
                sp_index += 1
                if sp_index > len(sps) - 1:  # loop around set point array if its end is reached
                    sp_index = 0

        tracking_error = np.sum(np.square(self.experiment_height-self.height_sp))
        return tracking_error
   
    def normalize(self, minmax_arr, val):
        val = np.clip(val, minmax_arr[0, :], minmax_arr[1, :])
        norm_val = (val - minmax_arr[0, :]) / (minmax_arr[1, :] - minmax_arr[0, :])
        return norm_val

    def denormalize(self, minmax_arr, norm_val):
        denorm = norm_val * (minmax_arr[1, :] - minmax_arr[0, :]) + minmax_arr[0, :]
        return denorm

