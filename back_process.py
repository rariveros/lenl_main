import cv2
import pandas as pd
import numpy as np
from numpy import genfromtxt
import os
import sys
import shutil
from scipy import signal
from scipy.signal import filtfilt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.stats import linregress
from scipy.fft import fft, fftfreq, fftshift
from scipy.signal import hilbert, chirp
import scipy.sparse as sparse
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.animation import FuncAnimation
from matplotlib.colors import TwoSlopeNorm
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import time
import winsound
import datetime
from matplotlib.colors import DivergingNorm
from scipy.signal import hilbert, chirp
from numpy import unravel_index

def pix_to_mm(img, scale):
    def click_event(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            points_i = (x, y)
            points.append(points_i)
            cv2.circle(img, (x, y), radius=4, color=(0, 0, 255), thickness=-1)
            cv2.imshow('image', img)
            if len(points) >= 2:
                cv2.line(img, (points[-1]), (points[-2]), (0, 255, 0), thickness=2, lineType=8)
                cv2.circle(img, (points[-1]), radius=4, color=(0, 0, 255), thickness=-1)
                cv2.circle(img, (points[-2]), radius=4, color=(0, 0, 255), thickness=-1)
            cv2.imshow('image', img)

    cv2.imshow('image', img)
    points = []
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    pix_to_mm = (40 / np.abs(points[-1][0] - points[-2][0])) * scale
    print('x_2=' + str(np.abs(points[-1][0])))
    print('x_1=' + str(np.abs(points[-2][0])))
    print('y_2=' + str(np.abs(points[-1][1])))
    print('y_1=' + str(np.abs(points[-2][1])))
    cv2.destroyAllWindows()
    return pix_to_mm


def sparse_D(Nx):
    data = np.ones((2, Nx))
    data[1] = -data[1]
    diags = [1, 0]
    D2 = sparse.spdiags(data, diags, Nx, Nx)
    D2 = sparse.lil_matrix(D2)
    D2[-1, -1] = 0
    return D2