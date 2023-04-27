"""
================================
Title:  mpc_kalman.py
Author: Antony Pulikapparambil
Date:   June 2022
================================
"""

import sys
import copy
import math
import numpy as np
from numpy import dot, zeros, eye, isscalar, shape
from scipy.linalg import cholesky
from scipy.stats import multivariate_normal
from scipy.optimize import minimize
from math import log, exp, sqrt
from copy import deepcopy

_support_singular = True        # for UKF
from client_classes import *

def system_model(xt, ut, A, B,
                 state_noise=None, measurement_noise=None, measurement_magnitude=np.array([[0], [0]])):
    """ System model used in MPC for moving horizon optimization """

    e1 = np.random.normal(np.array([[0], [0]]), state_noise) if state_noise is not None else np.array([[0], [0]])
    # A=0.98698487, B=0.00965852,
    if measurement_noise == 'truncated':  # truncated
        e2 = np.abs(np.random.normal(np.array([[0], [0]]), measurement_magnitude))
    elif measurement_noise == 'normal':  # normal
        e2 = np.random.normal(np.array([[0], [0]]), measurement_magnitude)
    # elif measurement_noise == 'skew':  # skew
    #     skew_gamma = 1
    #     skew_scale = measurement_magnitude
    #     skew_loc = - skew_scale * skew_gamma / np.sqrt(1 + skew_gamma ** 2) * np.sqrt(2 / np.pi)
    #     e2 = skewnorm.rvs(skew_gamma, loc=skew_loc, scale=skew_scale)
    # elif measurement_noise == 'skew2':  # skew
    #     skew_gamma = 2
    #     skew_scale = measurement_magnitude
    #     skew_loc = - skew_scale * skew_gamma / np.sqrt(1 + skew_gamma ** 2) * np.sqrt(2 / np.pi)
    #     e2 = skewnorm.rvs(skew_gamma, loc=skew_loc, scale=skew_scale)
    else:
        e2 = np.array([[0], [0]])

    C = np.array([[1, 0], [0, 1]])  # C is identity matrix (output y = state x)
    xtt = A @ xt + B @ ut + e1      # state equation + disturbance
    yt = C @ xtt + e2               # output equation + noise
    return xtt, yt

def nl_system_model(xt, ut):
    """SISO nonlinear model of system"""
    # Ball heights clipped between 0 and 100 cm
    xtt = np.clip(-68.6 + 0.92*xt + 1.8*ut, 0, 100)
    yt = xtt
    return xtt, yt

# ======== Linear/adaptive MIMO MPC ======== #

def mpc(Q, R, xk, N, umin, umax, xk_sp, A, B, P='none'):
    """ Determines optimal controller action using the set point error and model prediction """

    u_init = 50*np.ones((2, N))  # initial guess for input trajectory
    u_bounds = ((umin, umax),) * 2 * N  # bounds on the input trajectory
    # np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]])  #
    sol = minimize(mpc_obj, u_init, args=(Q, R, P, xk, N, xk_sp, A, B), method='SLSQP', bounds=u_bounds,
                   options={'eps': 1e-6, 'disp': False})
    # the optimized input trajectory is stored in sol.x
    U = np.reshape(sol.x, (2, N))
    # only the first input value is implemented according to receding horizon implementation
    uk = U[:, [0]]

    # bug: use these {U, x} for identification
    return uk, sol.fun


def mpc_obj(U, Q, R, P, xk, N, xk_sp, A, B):
    """ Calculates cost function for linear MPC """

    ukprev = np.array([[0], [0]])
    J = (xk - xk_sp).T @ Q @ (xk - xk_sp)
    U = np.reshape(U, (2, N))
    for k in range(0, N):
        # uk = U[:, [k]]  # this U is the optimized input trajectory by 'minimize' used in mpc function
        # xk, _ = system_model(xk, uk, A, B)
        # J += 0.5 * uk.T @ R @ uk + 0.5 * (xk - xk_sp).T @ Q @ (xk - xk_sp)

        # *OR put cost on CHANGE in controller output (added velocity term)
        uk = U[:, [k]]  # this U is the optimized input trajectory by 'minimize' used in mpc function
        du = uk - ukprev
        ukprev = uk
        xk, _ = system_model(xk, uk, A, B)
        J += 0.5 * (xk - xk_sp).T @ Q @ (xk - xk_sp) + 0.4 * uk.T @ R @ uk + 0.1 * du.T @ R @du

    # Terminal cost term (is ignored if 'P' is a string)
    if type(P) != str:
        J += 0.5 * (xk - xk_sp).T @ P @ (xk - xk_sp) - 0.5 * (xk - xk_sp).T @ Q @ (xk - xk_sp)
    return J.flatten()


def opt_func(x, data3, data2, data1):
    """ Optimizer used in adaptive MPC to update A and B """
    cost = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        A_ = np.asarray([[x[i][0], x[i][1]], [x[i][2], x[i][3]]])
        B_ = np.asarray([[x[i][4], x[i][5]], [x[i][6], x[i][7]]])
        cost[i] = np.sum((data3 - (A_ @ data1 + B_ @ data2)) ** 2)
    return cost


# ======== Nonlinear SISO MPC ======== #


def nl_mpc(Q, R, xk, N, umin, umax, xk_sp, P='none'):
    """ Determines optimal controller action using the set point error and model prediction """

    u_init = 50*np.ones(N)          # initial guess for input trajectory
    u_bounds = ((umin, umax),) * N  # bounds on the input trajectory
    sol = minimize(nl_mpc_obj, u_init, args=(Q, R, P, xk, N, xk_sp), method='SLSQP', bounds=u_bounds,
                   options={'eps': 1e-6, 'disp': False})
    # the optimized input trajectory is stored in sol.x
    # U = np.reshape(sol.x, (1, N))
    U = sol.x
    # only the first input value is implemented according to receding horizon implementation
    uk = U[0]

    # bug: use these {U, x} for identification
    return uk, sol.fun


def nl_mpc_obj(U, Q, R, P, xk, N, xk_sp):
    """ Calculates cost function for SISO NONLINEAR MPC """

    ukprev = 0
    J = (xk - xk_sp) * Q * (xk - xk_sp)
    # U = np.reshape(U, (1, N))
    for k in range(0, N):
        # uk = U[:, [k]]  # this U is the optimized input trajectory by 'minimize' used in mpc function
        # xk, _ = system_model(xk, uk, A, B)
        # J += 0.5 * uk.T @ R @ uk + 0.5 * (xk - xk_sp).T @ Q @ (xk - xk_sp)

        # *OR put cost on CHANGE in controller output (added velocity term)
        uk = U[k]  # this U is the optimized input trajectory by 'minimize' used in mpc function
        du = uk - ukprev
        ukprev = uk
        xk, _ = nl_system_model(xk, uk)
        J += 0.5*(xk - xk_sp)*Q*(xk - xk_sp) + 0.4*uk*R*uk + 0.1*du*R*du

    # Terminal cost term (is ignored if 'P' is a string)
    if type(P) != str:
        J += 0.5*(xk - xk_sp)*P*(xk - xk_sp) - 0.5*(xk - xk_sp)*Q*(xk - xk_sp)
    return J # J.flatten()

# ======== Kalman Filter ======== #


def logpdf(x, mean=None, cov=1, allow_singular=True):
    """
    Computes the log of the probability density function of the normal
    N(mean, cov) for the data x. The normal may be univariate or multivariate.
    Wrapper for older versions of scipy.multivariate_normal.logpdf which
    don't support support the allow_singular keyword prior to verion 0.15.0.
    If it is not supported, and cov is singular or not PSD you may get
    an exception.
    `x` and `mean` may be column vectors, row vectors, or lists.
    """

    if mean is not None:
        flat_mean = np.asarray(mean).flatten()
    else:
        flat_mean = None

    flat_x = np.asarray(x).flatten()

    if _support_singular:
        return multivariate_normal.logpdf(flat_x, flat_mean, cov, allow_singular)
    return multivariate_normal.logpdf(flat_x, flat_mean, cov)


def reshape_z(z, dim_z, ndim):
    """ ensure z is a (dim_z, 1) shaped vector"""

    z = np.atleast_2d(z)
    if z.shape[1] == dim_z:
        z = z.T

    if z.shape != (dim_z, 1):
        raise ValueError('z (shape {}) must be convertible to shape ({}, 1)'.format(z.shape, dim_z))

    if ndim == 1:
        z = z[:, 0]

    if ndim == 0:
        z = z[0, 0]

    return z

def h_cv(xt):
    """Output equation in state-space"""
    # y = x => C = 1
    return xt


def unscented_transform(sigmas, Wm, Wc, noise_cov=None, mean_fn=None, residual_fn=None):
    kmax, n = sigmas.shape

    try:
        if mean_fn is None:
            # new mean is just the sum of the sigmas * weight
            x = np.dot(Wm, sigmas)  # dot = \Sigma^n_1 (W[k]*Xi[k])
        else:
            x = mean_fn(sigmas, Wm)
    except:
        print(sigmas)
        raise

    if residual_fn is np.subtract or residual_fn is None:
        y = sigmas - x[np.newaxis, :]
        P = np.dot(y.T, np.dot(np.diag(Wc), y))
    else:
        P = np.zeros((n, n))
        for k in range(kmax):
            y = residual_fn(sigmas[k], x)
            P += Wc[k] * np.outer(y, y)

    if noise_cov is not None:
        P += noise_cov

    return (x, P)

class UnscentedKalmanFilter(object):
    def __init__(self, dim_x, dim_z, dt, hx, fx, points,
                 sqrt_fn=None, x_mean_fn=None, z_mean_fn=None,
                 residual_x=None,
                 residual_z=None,
                 state_add=None):

        self.x = np.zeros(dim_x)
        self.P = np.eye(dim_x)
        self.x_prior = np.copy(self.x)
        self.P_prior = np.copy(self.P)
        self.Q = np.eye(dim_x)
        self.R = np.eye(dim_z)
        self._dim_x = dim_x
        self._dim_z = dim_z
        self.points_fn = points
        self._dt = dt
        self._num_sigmas = points.num_sigmas()
        self.hx = hx
        self.fx = fx
        self.x_mean = x_mean_fn
        self.z_mean = z_mean_fn

        if sqrt_fn is None:
            self.msqrt = cholesky
        else:
            self.msqrt = sqrt_fn

        # weights for the means and covariances.
        self.Wm, self.Wc = points.Wm, points.Wc

        if residual_x is None:
            self.residual_x = np.subtract
        else:
            self.residual_x = residual_x

        if residual_z is None:
            self.residual_z = np.subtract
        else:
            self.residual_z = residual_z

        if state_add is None:
            self.state_add = np.add
        else:
            self.state_add = state_add

        # sigma points transformed through f(x) and h(x)
        # variables for efficiency so we don't recreate every update

        self.sigmas_f = np.zeros((self._num_sigmas, self._dim_x))
        self.sigmas_h = np.zeros((self._num_sigmas, self._dim_z))

        self.K = np.zeros((dim_x, dim_z))  # Kalman gain
        self.y = np.zeros((dim_z))  # residual
        self.z = np.array([[None] * dim_z]).T  # measurement
        self.S = np.zeros((dim_z, dim_z))  # system uncertainty
        self.SI = np.zeros((dim_z, dim_z))  # inverse system uncertainty

        self.inv = np.linalg.inv

        # these will always be a copy of x,P after predict() is called
        self.x_prior = self.x.copy()
        self.P_prior = self.P.copy()

        # these will always be a copy of x,P after update() is called
        self.x_post = self.x.copy()
        self.P_post = self.P.copy()

    def predict(self, dt=None, UT=None, fx=None, **fx_args):

        if dt is None:
            dt = self._dt

        if UT is None:
            UT = unscented_transform

        # calculate sigma points for given mean and covariance
        self.compute_process_sigmas(dt, fx, **fx_args)

        # and pass sigmas through the unscented transform to compute prior
        self.x, self.P = UT(self.sigmas_f, self.Wm, self.Wc, self.Q,
                            self.x_mean, self.residual_x)

        # update sigma points to reflect the new variance of the points
        self.sigmas_f = self.points_fn.sigma_points(self.x, self.P)

        # save prior
        self.x_prior = np.copy(self.x)
        self.P_prior = np.copy(self.P)

    def update(self, z, R=None, UT=None, hx=None, **hx_args):

        if z is None:
            self.z = np.array([[None] * self._dim_z]).T
            self.x_post = self.x.copy()
            self.P_post = self.P.copy()
            return

        if hx is None:
            hx = self.hx

        if UT is None:
            UT = unscented_transform

        if R is None:
            R = self.R
        elif np.isscalar(R):
            R = np.eye(self._dim_z) * R

        sigmas_h = []
        for s in self.sigmas_f:
            sigmas_h.append(hx(s, **hx_args))

        self.sigmas_h = np.atleast_2d(sigmas_h)

        # mean and covariance of prediction passed through unscented transform
        zp, self.S = UT(self.sigmas_h, self.Wm, self.Wc, R, self.z_mean, self.residual_z)
        self.SI = self.inv(self.S)

        # compute cross variance of the state and the measurements
        Pxz = self.cross_variance(self.x, zp, self.sigmas_f, self.sigmas_h)

        self.K = np.dot(Pxz, self.SI)  # Kalman gain
        self.y = self.residual_z(z, zp)  # residual

        # update Gaussian state estimate (x, P)
        self.x = self.state_add(self.x, np.dot(self.K, self.y))
        self.P = self.P - np.dot(self.K, np.dot(self.S, self.K.T))

        # save measurement and posterior state
        self.z = copy.deepcopy(z)
        self.x_post = self.x.copy()
        self.P_post = self.P.copy()

        # set to None to force recompute
        self._log_likelihood = None
        self._likelihood = None
        self._mahalanobis = None

    def cross_variance(self, x, z, sigmas_f, sigmas_h):
        Pxz = np.zeros((sigmas_f.shape[1], sigmas_h.shape[1]))
        N = sigmas_f.shape[0]
        for i in range(N):
            dx = self.residual_x(sigmas_f[i], x)
            dz = self.residual_z(sigmas_h[i], z)
            Pxz += self.Wc[i] * np.outer(dx, dz)
        return Pxz

    def compute_process_sigmas(self, dt, fx=None, **fx_args):
        if fx is None:
            fx = self.fx

        # calculate sigma points for given mean and covariance
        sigmas = self.points_fn.sigma_points(self.x, self.P)

        for i, s in enumerate(sigmas):
            self.sigmas_f[i], _ = fx(s, dt, **fx_args)

    def batch_filter(self, zs, Rs=None, dts=None, UT=None, saver=None):

        try:
            z = zs[0]
        except TypeError:
            raise TypeError('zs must be list-like')

        if self._dim_z == 1:
            if not (np.isscalar(z) or (z.ndim == 1 and len(z) == 1)):
                raise TypeError('zs must be a list of scalars or 1D, 1 element arrays')
        else:
            if len(z) != self._dim_z:
                raise TypeError(
                    'each element in zs must be a 1D array of length {}'.format(self._dim_z))

        z_n = np.size(zs, 0)
        if Rs is None:
            Rs = [self.R] * z_n

        if dts is None:
            dts = [self._dt] * z_n

        # mean estimates from Kalman Filter
        if self.x.ndim == 1:
            means = np.zeros((z_n, self._dim_x))
        else:
            means = np.zeros((z_n, self._dim_x, 1))

        # state covariances from Kalman Filter
        covariances = np.zeros((z_n, self._dim_x, self._dim_x))

        for i, (z, r, dt) in enumerate(zip(zs, Rs, dts)):
            self.predict(dt=dt, UT=UT)
            self.update(z, r, UT=UT)
            means[i, :] = self.x
            covariances[i, :, :] = self.P

            if saver is not None:
                saver.save()

        return (means, covariances)

    def rts_smoother(self, Xs, Ps, Qs=None, dts=None, UT=None):
        if len(Xs) != len(Ps):
            raise ValueError('Xs and Ps must have the same length')

        n, dim_x = Xs.shape

        if dts is None:
            dts = [self._dt] * n
        elif np.isscalar(dts):
            dts = [dts] * n

        if Qs is None:
            Qs = [self.Q] * n

        if UT is None:
            UT = unscented_transform

        # smoother gain
        Ks = np.zeros((n, dim_x, dim_x))

        num_sigmas = self._num_sigmas

        xs, ps = Xs.copy(), Ps.copy()
        sigmas_f = np.zeros((num_sigmas, dim_x))

        for k in reversed(range(n - 1)):
            # create sigma points from state estimate, pass through state func
            sigmas = self.points_fn.sigma_points(xs[k], ps[k])
            for i in range(num_sigmas):
                sigmas_f[i] = self.fx(sigmas[i], dts[k])

            xb, Pb = UT(
                sigmas_f, self.Wm, self.Wc, self.Q,
                self.x_mean, self.residual_x)

            # compute cross variance
            Pxb = 0
            for i in range(num_sigmas):
                y = self.residual_x(sigmas_f[i], xb)
                z = self.residual_x(sigmas[i], Xs[k])
                Pxb += self.Wc[i] * np.outer(z, y)

            # compute gain
            K = np.dot(Pxb, self.inv(Pb))

            # update the smoothed estimates
            xs[k] += np.dot(K, self.residual_x(xs[k + 1], xb))
            ps[k] += np.dot(K, ps[k + 1] - Pb).dot(K.T)
            Ks[k] = K

        return (xs, ps, Ks)

    @property
    def log_likelihood(self):

        if self._log_likelihood is None:
            self._log_likelihood = logpdf(x=self.y, cov=self.S)
        return self._log_likelihood

    @property
    def likelihood(self):

        if self._likelihood is None:
            self._likelihood = math.exp(self.log_likelihood)
            if self._likelihood == 0:
                self._likelihood = sys.float_info.min
        return self._likelihood

    @property
    def mahalanobis(self):

        if self._mahalanobis is None:
            self._mahalanobis = math.sqrt(float(np.dot(np.dot(self.y.T, self.SI), self.y)))
        return self._mahalanobis


class SimplexSigmaPoints(object):

    def __init__(self, n, alpha=1, sqrt_method=None, subtract=None):
        self.n = n
        self.alpha = alpha
        if sqrt_method is None:
            self.sqrt = cholesky
        else:
            self.sqrt = sqrt_method

        if subtract is None:
            self.subtract = np.subtract
        else:
            self.subtract = subtract

        self._compute_weights()

    def num_sigmas(self):
        """ Number of sigma points for each variable in the state x"""
        return self.n + 1

    def sigma_points(self, x, P):

        if self.n != np.size(x):
            raise ValueError("expected size(x) {}, but size is {}".format(
                self.n, np.size(x)))

        n = self.n

        if np.isscalar(x):
            x = np.asarray([x])
        x = x.reshape(-1, 1)

        if np.isscalar(P):
            P = np.eye(n) * P
        else:
            P = np.atleast_2d(P)

        U = self.sqrt(P)

        lambda_ = n / (n + 1)
        Istar = np.array([[-1 / np.sqrt(2 * lambda_), 1 / np.sqrt(2 * lambda_)]])

        for d in range(2, n + 1):
            row = np.ones((1, Istar.shape[1] + 1)) * 1. / np.sqrt(
                lambda_ * d * (d + 1))  # pylint: disable=unsubscriptable-object
            row[0, -1] = -d / np.sqrt(lambda_ * d * (d + 1))
            Istar = np.r_[np.c_[Istar, np.zeros((Istar.shape[0]))], row]  # pylint: disable=unsubscriptable-object

        I = np.sqrt(n) * Istar
        scaled_unitary = (U.T).dot(I)

        sigmas = self.subtract(x, -scaled_unitary)
        return sigmas.T

    def _compute_weights(self):
        """ Computes the weights for the scaled unscented Kalman filter. """

        n = self.n
        c = 1. / (n + 1)
        self.Wm = np.full(n + 1, c)
        self.Wc = self.Wm

# results = reader.calibrate()
# print(results)
# def foo(my_int=2, my_str='None'):
#     print(my_str)
#     return np.zeros(my_int)

# def foo2(my_int):
#     return my_int

# with cf.ThreadPoolExecutor(max_workers=2) as executor:
#     futures = [executor.submit(foo, 2, 'hello'), executor.submit(foo2,10)]
#     for future in cf.as_completed(futures):
#         print(future.result())
    


# model = YOLO("./Data/Object_Detection/Small/best2.pt")
# video_url = 'http://admin:LogDeltav50@142.244.38.73/video/mjpg.cgi'
# distortion_path = './Distortion/*.jpg'

# cap = cv2.VideoCapture(video_url)

# # termination criteria
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# objp = np.zeros((5 * 10, 3), np.float32)
# objp[:, :2] = np.mgrid[0:10, 0:5].T.reshape(-1, 2)
# objp = objp * 2.9

# # Arrays to store object points and image points from all the images.
# objpoints = [] # 3d point in real world space
# imgpoints = [] # 2d points in image plane.

# images = glob.glob(distortion_path)
# for fname in images:
#     img = cv2.imread(fname)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, corners = cv2.findChessboardCorners(gray, (10, 5), None)
    
#     # If found, add object points, image points (after refining them)
#     if ret == True:
#         objpoints.append(objp)
#         corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
#         imgpoints.append(corners2)

# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# sample_start = time.time()
# ret, frame = cap.read()
# height, width = frame.shape[:2]

# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))
# undist_image = cv2.undistort(frame, mtx, dist, None, newcameramtx)
# x, y, w, h = roi
# undist_image = undist_image[y:y+h, x:x+w]
# frame = undist_image[20:600, 400:600]

# # Display the resulting frame
# if ret:
#     results = model.predict(source=frame, show=False, conf=0.60, hide_labels=True, max_det=4)
#     print(results[0].boxes.xywh)
#     print(time.time() - sample_start)

# for i in range(2):
#     sample_start = time.time()
#     ret, frame = cap.read()
#     height, width = frame.shape[:2]

#     newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))
#     undist_image = cv2.undistort(frame, mtx, dist, None, newcameramtx)
#     x, y, w, h = roi
#     undist_image = undist_image[y:y+h, x:x+w]
#     frame = undist_image[20:600, 400:600]

#     # Display the resulting frame
#     if ret:
#         results = model.predict(source=frame, show=False, conf=0.60, hide_labels=True, max_det=4)
#         print(results[0].boxes.xywh)
#         print(time.time() - sample_start)

# cap.release()
