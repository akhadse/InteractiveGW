import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import cv2
import gwsurrogate
from flask import render_template, jsonify
#######################################################
sur   = gwsurrogate.LoadSurrogate("NRSur7dq4")
times = np.arange(-4299,99,1)
f_low = 0
#######################################################


def generate_strain_for_param(input_dict):

    q     = input_dict["q"]
    chiA0 = np.array([input_dict["chiAx"], input_dict["chiAy"], input_dict["chiAz"]])
    chiB0 = np.array([input_dict["chiBx"] , input_dict["chiBy"], input_dict["chiBz"]])

    inclination = input_dict["inclination"] *np.pi/180
    phi_ref     = input_dict["phi_ref"] *np.pi/180

    t,h,dyn = sur(q, chiA0, chiB0, inclination=inclination,phi_ref=phi_ref, f_low=f_low, times=times)

    h_plus  =  np.real(h) 
    h_cross = -np.imag(h)
    h_abs   =  np.abs(h)

    h_plus  = h_plus.tolist()
    h_cross = h_cross.tolist()
    h_abs   = h_abs.tolist()
    t       = t.tolist()

    return jsonify({'times':t, 'h_plus': h_plus, 'h_cross':h_cross, 'h_abs':h_abs})

def generate_sur_h_lm_for_param(input_dict):

    q     = input_dict["q"]
    chiA0 = np.array([input_dict["chiAx"], input_dict["chiAy"], input_dict["chiAz"]])
    chiB0 = np.array([input_dict["chiBx"] , input_dict["chiBy"], input_dict["chiBz"]])

    t,h,dyn = sur(q, chiA0, chiB0, f_low=f_low, times=times)

    l = input_dict["l"]
    m = input_dict["m"]

    h_lm = h[(l,m)]

    h_lm_real = np.real(h_lm)
    h_lm_real = h_lm_real.tolist()
    h_lm_imag = np.imag(h_lm)
    h_lm_imag = h_lm_imag.tolist()
    h_lm_abs  = np.abs(h_lm)
    h_lm_abs  = h_lm_abs.tolist()
    t = t.tolist()
    return jsonify({'times':t, 'h_lm_real': h_lm_real, 'h_lm_imag':h_lm_imag, 'h_lm_abs':h_lm_abs})
