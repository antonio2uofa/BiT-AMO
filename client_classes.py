import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ultralytics import YOLO
from cycler import cycler
from typing import List
from datetime import datetime

import asyncio
import glob
import cv2
import multiprocessing as mp

CAM_URL = 'http://142.244.38.73/image/jpeg.cgi'
PDF_PATH = './Data/bit_data/bit_plot.pdf'
MODEL_PATH = './Data/bit_data/bit_data_model.csv'

"""
Plotter class to be used with client when processing and plotting BiT data.
"""
class Plotter:
    def __init__(self, sampling_array, time_array, level_array,
    fanspeed_array, height_sp, custom_cycler=None):

        self.sampling_array = sampling_array
        self.time_array = time_array
        self.level_array = level_array
        self.fanspeed_array = fanspeed_array
        self.height_sp = height_sp
        self.header = [
            "Fan #4", "Fan #3", "Fan #2", "Fan #1",
            "Level #4", "Level #3", "Level #2",
            "Time (s)",
            ]
    """
    Creates two separate plots that contain the fanspeeds and levels of 3 the tubes
    respectively.
    """
    def double_plot(self, pdf_path=PDF_PATH):
            
        fs_lines, level_lines = [], []

        fig, axs = plt.subplots(2, sharex='all', figsize=(12, 7))  # OD
        fig.suptitle('Y and U Plots')

        for subplt in axs:
            subplt.xaxis.set_major_formatter(plt.FormatStrFormatter('% .2f'))
            subplt.yaxis.set_major_formatter(plt.FormatStrFormatter('% .2f'))

        fs_lines = axs[0].plot(self.time_array, self.fanspeed_array, ls='-.', label='position')
        level_lines = axs[1].plot(self.time_array, self.level_array, ls='--', label='position')
        # axs[1].plot(self.time_array, self.height_sp)
        axs[0].legend(
        	fs_lines, ["Fan 4", "Fan 3", " Fan 2", "Fan 1"], loc='upper center',
        	bbox_to_anchor=(0.5, 1.15), ncol=4, fancybox=True, shadow=True,
        	)      
        axs[1].legend(
        	level_lines, ["Level 4", " Level 3", " Level 2"], loc='upper center', 
        	bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True,
        	)   
        axs[1].set_xlabel('Time (s)') #OD
        axs[1].set_ylabel('Level (us)') #OD
        axs[0].set_ylabel('Fan Speed (rpm)') #OD
        
        # fig.tight_layout()
        plt.show()
        plt.savefig(pdf_path)

    """
    Create 6 subplots to split fanspeeds, levels, and setpoint into separate plots.
    """
    def triple_plot(self, pdf_path=PDF_PATH):
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fig, ax = plt.subplots(2,3, figsize=(10, 7), sharex='all', constrained_layout=True)

        ax[0,0].plot(self.time_array, np.array(self.level_array)[:,0], '-.', color='tab:blue', alpha=0.5, label='True Height')
        ax[0,0].plot(self.time_array, np.array(self.height_sp)[:,0], '-', color='k', alpha=0.5, label='Set Point')
        ax[1,0].plot(self.time_array, np.array(self.fanspeed_array)[:,0], '.-', color='tab:red', alpha=0.5)
        ax[0,0].legend()

        ax[0,1].plot(self.time_array, np.array(self.level_array)[:,1], '-.', color='tab:blue', alpha=0.5, label='True Height')
        ax[0,1].plot(self.time_array, np.array(self.height_sp)[:,1], '-', color='k', alpha=0.5, label='Set Point')
        ax[1,1].plot(self.time_array, np.array(self.fanspeed_array)[:,1], '.-', color='tab:red', alpha=0.5)
        ax[0,1].legend()

        ax[0,2].plot(self.time_array, np.array(self.level_array)[:,2], '-.', color='tab:blue', alpha=0.5, label='True Height')
        ax[0,2].plot(self.time_array, np.array(self.height_sp)[:,2], '-', color='k', alpha=0.5, label='Set Point')
        ax[1,2].plot(self.time_array, np.array(self.fanspeed_array)[:,2], '.-', color='tab:red', alpha=0.5)
        ax[0,2].legend()
        ax[1,1].set_title(f'Fan Speed Factor')
        ax[0,1].set_title(f'Ball Heights [cm]')

        fig.suptitle(f'BiT Simulation - MPC Test ({curr_datetime})', fontsize=12)

        plt.tight_layout()
        plt.savefig(pdf_path, bbox_inches='tight')  # Save the plot as a pdf file
        plt.show()

    def data_to_csv(self, csv_path: str):
        # Exporting data to .csv file using pandas.
        fanspeed_df = pd.DataFrame(self.fanspeed_array)
        level_df = pd.DataFrame(self.level_array)
        time_df = pd.DataFrame(self.time_array)

        result = pd.concat([fanspeed_df, level_df, time_df], axis=1)
        result.to_csv(csv_path, float_format='%.1f', mode='w', header=self.header, index=False)

"""
Class to wrap all image processing functions.
"""
class Reader:
    def __init__(self, csv_path: str):
        # Initialized for distortion matrix
        self.distortion_path: str = './Distortion/*.jpg'
        self.ret, self.mtx, self.dist = self._get_distortion_mat()

        #Initialized for image detection
        self.model = YOLO("./Data/Object_Detection/Small/best2.pt")  # load a custom model

        # Initialized for read_fan_gains
        self.csv_path: str = csv_path
        self.fan_gain_df = pd.read_csv(csv_path)

        # Initialized for read_frames
        self.count: int = 0
        self.video_url: str = 'http://admin:LogDeltav50@142.244.38.73/video/mjpg.cgi'
        self.cap = cv2.VideoCapture(self.video_url)

    def _get_distortion_mat(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((5*10,3), np.float32)
        objp[:,:2] = np.mgrid[0:10,0:5].T.reshape(-1,2)
        objp = objp * 2.9
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        images = glob.glob(self.distortion_path)
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (10,5), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        return ret, mtx, dist

    def rm_distortion(self, dist_image):
        # read distorted image & get new matrix
        h,  w = dist_image.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
        # undistort image
        undist_image = cv2.undistort(dist_image, self.mtx, self.dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        undist_image = undist_image[y:y+h, x:x+w]
        cv2.imwrite('calibresult.png', undist_image)
        return undist_image

    def track_balls(self, image):
        cropped = image[0:434, 350:630]
        results = self.model.predict(source=cropped, save=True)
        return results

    def read_fan_gains(self):
        headers = list(self.fan_gain_df.columns.values)

        tube4_gains = self.fan_gain_df[f"{headers[0]}"].to_list()
        tube3_gains = self.fan_gain_df[f"{headers[1]}"].to_list()
        tube2_gains = self.fan_gain_df[f"{headers[2]}"].to_list()
        tube1_gains = self.fan_gain_df[f"{headers[3]}"].to_list()
        return tube4_gains, tube3_gains, tube2_gains, tube1_gains

    def read_frames(self, path_to_folder="./Data/Images/"):

        # Read a frame from the camera
        for i in range(1):
            ret, frame = self.cap.read()
            #Remove the distortion
            if ret:
                frame = self.rm_distortion(frame)
            # Perform ball detection/tracking using YOLOv8
            results = self.track_balls(frame)
            cv2.imwrite('{0}result{1}.jpg'.format(path_to_folder, self.count), frame)
            self.count += 1

    # Ensures that we release the camera feed
    def __del__(self):
        self.cap.release()

async def sample(ns_idx, bit_obj, gain4, gain3, gain2, gain1, normalized=False, stall=0):
    await bit_obj.call_method(f"{ns_idx}:set_fanspeeds", gain4, gain3, gain2, gain1, normalized)
    await asyncio.sleep(stall)

    fanspeed_array = np.array(await bit_obj.call_method(f"{ns_idx}:get_fanspeeds"))
    level_array = np.array([
        await bit_obj.call_method(f"{ns_idx}:get_level", 4),
        await bit_obj.call_method(f"{ns_idx}:get_level", 3),
        await bit_obj.call_method(f"{ns_idx}:get_level", 2),
    ])
    return fanspeed_array, level_array

async def calibrate(ns_idx, bit_obj, stall=1):
    maxmin_array = [np.zeros((10, 3)) for i in range(4)]
    for i in range(10):
        print(f"Loop number: {i}")
        speed_max, level_min = await sample(ns_idx, bit_obj, 0, 0, 0, 100, normalized=False, stall=stall)
        maxmin_array[0][i] = speed_max[0:3]
        maxmin_array[3][i] = level_min

        speed_min, level_max = await sample(ns_idx, bit_obj, 100, 100, 100, 100, normalized=False, stall=stall)
        maxmin_array[1][i] = speed_min[0:3]
        maxmin_array[2][i] = level_max

    maxmin_mean = [np.mean(array, axis=0) for array in maxmin_array]
    return maxmin_mean

