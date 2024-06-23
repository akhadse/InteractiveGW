import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import cv2
import gwsurrogate
from flask import render_template, jsonify
import time
from datetime import date,timedelta
from matplotlib.animation import FuncAnimation, writers
import random
import string
import os

from matplotlib.animation import FFMpegWriter
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
#######################################################
sur   = gwsurrogate.LoadSurrogate("NRSur7dq4")
times = np.arange(-4299,99,1)
f_low = 0
#######################################################
import boto3
s3=boto3.client('s3', region_name='us-east-2')

def generate_presigned_url(video_name):
    bucket_name = 'interactivegwbucket'
    key_name = video_name 
    s3.upload_file(os.getcwd()+'/downloaded_videos/'+ video_name, bucket_name, key_name)
    presigned_url = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': key_name},ExpiresIn=300)
    #presigned_url = filename # will link to the video on S3
    filename = os.getcwd()+'/downloaded_videos/'+ video_name
    os.system(f"rm -rf {filename}")
    return presigned_url
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


def generate_video_for_strain_for_varying_param_method_2(input_dict):
    start_time = time.time()

    ################
    allowed_params_to_vary = ['q','chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz', 'inclination', 'phi_ref']
    ################
    user_input       = input_dict["user_input"]
    surrogate_params = input_dict["surrogate_params"]
    video_params     = input_dict["video_params"]
    figure_params    = input_dict["figure_params"]

    video_width = video_params["video_width"]
    video_height = video_params["video_height"]
    video_fps = video_params["video_fps"]
    video_name = video_params["video_name"]

    DPI = 100 # dots per inch
    figure_width = video_width/DPI
    figure_height = video_height/DPI
    figsize       = (figure_width,figure_height)

    # Get user input values
    choose_parameter_to_vary     = user_input["choose_parameter_to_vary"]     # Choose from 'q', 'chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz'
    parameter_start_value        = user_input["parameter_start_value"]
    parameter_end_value          = user_input["parameter_end_value"]
    parameter_steps              = user_input["parameter_steps"] # performs at around 5 steps/second

    inclination=user_input["inclination"]
    phi_ref=user_input["phi_ref"]

    # Surrogate parameters
    sur_name   = surrogate_params["sur_name"]  
    f_low = surrogate_params["f_low"]
    delta_t = surrogate_params["delta_t"]
    
    sur   = gwsurrogate.LoadSurrogate(sur_name)
    times = np.arange(-4299,99,delta_t)

    #
    fixed_params = [i for i in allowed_params_to_vary if i!=choose_parameter_to_vary]

    parameter_to_vary_values = np.linspace(parameter_start_value,parameter_end_value,parameter_steps)

    i = 0
    for param_val in parameter_to_vary_values:

        user_input[choose_parameter_to_vary] = param_val

        q     = user_input["q"]
        chiA0 = np.array([user_input["chiAx"],user_input["chiAy"],user_input["chiAz"]])
        chiB0 = np.array([user_input["chiBx"],user_input["chiBy"],user_input["chiBz"]])

        inclination = user_input["inclination"] *np.pi/180
        phi_ref     = user_input["phi_ref"] *np.pi/180

        chiAmag = np.sqrt(np.sum(chiA0**2))
        chiBmag = np.sqrt(np.sum(chiB0**2))

        if chiAmag<=1 and chiBmag<=1:
  
            t,h,dyn = sur(q, chiA0, chiB0, inclination=inclination,phi_ref=phi_ref, f_low=f_low, times=times)

            h_plus  =  np.real(h) 
            h_cross = -np.imag(h)
            h_abs   =  np.abs(h)

            if i==0:
                i+=1
                h_max_initial_param = np.max(h_abs)
                y_max = 1.1*h_max_initial_param
                y_min = -y_max
                
                data_h_plus  = np.zeros((1,len(h_plus)))
                data_h_cross = np.zeros((1,len(h_cross)))
                data_h_abs   = np.zeros((1,len(h_abs)))
                all_parameter_values = np.zeros((1,9))
                varying_param_values = np.array([])

            data_h_plus          = np.vstack((data_h_plus, h_plus))
            data_h_cross         = np.vstack((data_h_cross, h_cross))
            data_h_abs           = np.vstack((data_h_abs, h_abs))
            all_parameter_values = np.vstack((all_parameter_values, np.array([q,chiA0[0], chiA0[1], chiA0[2],chiB0[0], chiB0[1], chiB0[2], inclination, phi_ref ])))
            varying_param_values = np.append(varying_param_values,param_val)
                   
    data_h_plus          = data_h_plus[1:,:]
    data_h_cross         = data_h_cross[1:,:]
    data_h_abs           = data_h_abs[1:,:]
    all_parameter_values = all_parameter_values[1:,:] 


    f, ((a0, a1), (a2, a3), (a4, a5)) = plt.subplots(3, 2, figsize=figsize, gridspec_kw={'width_ratios': [3, 1]})

    #-----------------------------------------------------------------------------------------------------------------------------
    a0.plot(t,data_h_plus[0,:], label='Initial_parameter', color='red', linewidth='0.8')
    a0.set_xlim((t[0],t[-1]))
    a0.set_ylim((y_min,y_max))
    a0.set_xlabel("Time (M)")
    a0.set_ylabel(r"$h_{+}$")
    a0.grid(axis='x')

    a1.plot(t,data_h_plus[0,:], label='real_initial_parameter', color='red', linewidth='0.8')
    a1.set_xlim((-200,50))
    a1.set_ylim((y_min,y_max))
    a1.set_xlabel("Time (M)")
    a1.grid(axis='x')
    #-----------------------------------------------------------------------------------------------------------------------------

    a2.plot(t,data_h_cross[0,:], label='imag_initial_parameter', color='red', linewidth='0.8')
    a2.set_xlim((t[0],t[-1]))
    a2.set_ylim((y_min,y_max))  
    a2.set_xlabel("Time (M)")
    a2.set_ylabel(r"$h_{\times}$")
    a2.grid(axis='x')

    a3.plot(t,data_h_cross[0,:], label='imag_initial_parameter', color='red', linewidth='0.8')
    a3.set_xlim((-200,50))
    a3.set_ylim((y_min,y_max))
    a3.set_xlabel("Time (M)")
    a3.grid(axis='x')

    #-----------------------------------------------------------------------------------------------------------------------------
    a4.plot(t,data_h_abs[0,:], label='abs_initial_parameter', color='red', linewidth='0.8')
    a4.set_xlim((t[0],t[-1]))
    a4.set_ylim((0.,y_max))   
    a4.set_xlabel("Time (M)")
    a4.set_ylabel(r"$ \mid h_{+} - i h_{\times}\mid $")
    a4.grid(axis='x')

    a5.plot(t,data_h_abs[0,:], label='abs_initial_parameter', color='red', linewidth='0.8')
    a5.set_xlim((-200,50))
    a5.set_ylim((0.,y_max))
    a5.set_xlabel("Time (M)")
    a5.grid(axis='x')

    plot_title = plt.suptitle(f"rh/M for {choose_parameter_to_vary} = {varying_param_values[0]:.2f} \n \n", fontsize=28, color='black', weight='bold')
    
    initial_param_text = f.text(0.025, 0.885,  f"Initial    -----> q = {all_parameter_values[0,0]:.2f}, chiA = ({all_parameter_values[0,1]:.2f} ,{all_parameter_values[0,2]:.2f} ,{all_parameter_values[0,3]:.2f}), chiB = ({all_parameter_values[0,4]:.2f} ,{all_parameter_values[0,5]:.2f} ,{all_parameter_values[0,6]:.2f}), inclination = {all_parameter_values[0,7]*180/np.pi:.0f}, phi_ref ={all_parameter_values[0,8]*180/np.pi:.0f}°",ha="left", va="center", fontsize=18, color='red')
    final_param_text   = f.text(0.025, 0.845 ,  f"Current -----> q = {  all_parameter_values[0,0]:.2f}, chiA = ({all_parameter_values[0,1]:.2f} ,{all_parameter_values[0,2]:.2f} ,{all_parameter_values[0,3]:.2f}), chiB = ({all_parameter_values[0,4]:.2f} ,{all_parameter_values[0,5]:.2f} ,{all_parameter_values[0,6]:.2f}), inclination = {all_parameter_values[0,7]*180/np.pi:.0f}, phi_ref ={all_parameter_values[0,8]*180/np.pi:.0f}°",ha="left", va="center", fontsize=18, color='#1f77b4')
    
    # Plot and store the line objects
    line0, = a0.plot(t, data_h_plus[0, :], label='Current_parameter')
    line1, = a1.plot(t, data_h_plus[0, :] )
    line2, = a2.plot(t, data_h_cross[0, :])
    line3, = a3.plot(t, data_h_cross[0, :])
    line4, = a4.plot(t, data_h_abs[0, :]  )
    line5, = a5.plot(t, data_h_abs[0, :]  )
    
    a0.legend(loc='upper left')
    f.tight_layout()

    def update(frame):
        # Update the data for each line object
        line0.set_ydata(data_h_plus[frame, :])
        line1.set_ydata(data_h_plus[frame, :])
        line2.set_ydata(data_h_cross[frame, :])
        line3.set_ydata(data_h_cross[frame, :])
        line4.set_ydata(data_h_abs[frame, :])
        line5.set_ydata(data_h_abs[frame, :])
        
        plot_title.set_text(f"rh/M for {choose_parameter_to_vary} = {varying_param_values[frame]:.2f} \n \n")
        final_param_text.set_text(f"Current -----> q = {  all_parameter_values[frame,0]:.2f}, chiA = ({all_parameter_values[frame,1]:.2f} ,{all_parameter_values[frame,2]:.2f} ,{all_parameter_values[frame,3]:.2f}), chiB = ({all_parameter_values[frame,4]:.2f} ,{all_parameter_values[frame,5]:.2f} ,{all_parameter_values[frame,6]:.2f}), inclination = {all_parameter_values[frame,7]*180/np.pi:.0f}°, phi_ref ={all_parameter_values[frame,8]*180/np.pi:.0f}°")
               
        return [line0, line1, line2, line3, line4, line5, plot_title,final_param_text ]

    ani = FuncAnimation(f, update, frames=data_h_plus.shape[0], blit=False)

    FFMpegWriter = writers['ffmpeg']
    writer = FFMpegWriter(fps=video_fps, metadata=dict(artist='Akshay Khadse'), bitrate=10000)
    
    video_filepath = os.getcwd()+'/downloaded_videos/'+video_name
    ani.save(video_filepath, writer=writer)

    runtime = time.time()-start_time
    runtime = str(timedelta(seconds = runtime))
    print("==========================================================")
    print("Video Downloaded in : ",runtime)
    print("==========================================================")
    return generate_presigned_url(video_name)

def generate_video_for_h_lm_varying_param_method_2(input_dict):
    start_time = time.time()

    ################
    allowed_params_to_vary = ['q','chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz']
    ################
    user_input       = input_dict["user_input"]
    surrogate_params = input_dict["surrogate_params"]
    video_params     = input_dict["video_params"]
    figure_params    = input_dict["figure_params"]

    video_width = video_params["video_width"]
    video_height = video_params["video_height"]
    video_fps = video_params["video_fps"]
    video_name = video_params["video_name"]

    DPI = 100 # dots per inch
    figure_width = video_width/DPI
    figure_height = video_height/DPI
    figsize       = (figure_width,figure_height)


    # Get user input values
    choose_parameter_to_vary     = user_input["choose_parameter_to_vary"]     # Choose from 'q', 'chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz'
    parameter_start_value        = user_input["parameter_start_value"]
    parameter_end_value          = user_input["parameter_end_value"]
    parameter_steps              = user_input["parameter_steps"] # performs at around 5 steps/second

    l=user_input["l"]
    m=user_input["m"]

    # Surrogate parameters
    sur_name   = surrogate_params["sur_name"]  
    f_low = surrogate_params["f_low"]
    delta_t = surrogate_params["delta_t"]
    
    sur   = gwsurrogate.LoadSurrogate(sur_name)
    times = np.arange(-4299,99,delta_t)

    #
    fixed_params = [i for i in allowed_params_to_vary if i!=choose_parameter_to_vary]

    parameter_to_vary_values = np.linspace(parameter_start_value,parameter_end_value,parameter_steps)

    i = 0
    for param_val in parameter_to_vary_values:

        user_input[choose_parameter_to_vary] = param_val

        q     = user_input["q"]
        chiA0 = np.array([user_input["chiAx"],user_input["chiAy"],user_input["chiAz"]])
        chiB0 = np.array([user_input["chiBx"],user_input["chiBy"],user_input["chiBz"]])

        chiAmag = np.sqrt(np.sum(chiA0**2))
        chiBmag = np.sqrt(np.sum(chiB0**2))

        if chiAmag<=1 and chiBmag<=1:
  
            t,h,dyn = sur(q, chiA0, chiB0, f_low=f_low, times=times)

            h_lm_real  = np.real(h[(l,m)])
            h_lm_imag  = np.imag(h[(l,m)])
            h_abs      = np.abs(h[(l,m)])

            if i==0:
                i+=1
                h_max_initial_param = np.max(h_abs)
                y_max = 1.1*h_max_initial_param
                y_min = -y_max
                
                data_h_lm_real  = np.zeros((1,len(h_lm_real)))
                data_h_lm_imag = np.zeros((1,len(h_lm_imag)))
                data_h_abs   = np.zeros((1,len(h_abs)))
                all_parameter_values = np.zeros((1,7))
                varying_param_values = np.array([])

            data_h_lm_real          = np.vstack((data_h_lm_real, h_lm_real))
            data_h_lm_imag         = np.vstack((data_h_lm_imag, h_lm_imag))
            data_h_abs           = np.vstack((data_h_abs, h_abs))
            all_parameter_values = np.vstack((all_parameter_values, np.array([q,chiA0[0], chiA0[1], chiA0[2],chiB0[0], chiB0[1], chiB0[2]])))
            varying_param_values = np.append(varying_param_values,param_val)
                   
    data_h_lm_real          = data_h_lm_real[1:,:]
    data_h_lm_imag         = data_h_lm_imag[1:,:]
    data_h_abs           = data_h_abs[1:,:]
    all_parameter_values = all_parameter_values[1:,:] 


    f, ((a0, a1), (a2, a3), (a4, a5)) = plt.subplots(3, 2, figsize=figsize, gridspec_kw={'width_ratios': [3, 1]})

    #-----------------------------------------------------------------------------------------------------------------------------
    a0.plot(t,data_h_lm_real[0,:], label='Initial_parameter', color='red', linewidth='0.8')
    a0.set_xlim((t[0],t[-1]))
    a0.set_ylim((y_min,y_max))
    a0.set_xlabel("Time")
    a0.set_ylabel(r"$\Re(h_{" + str(l) + str(m) + "})$")
    a0.grid(axis='x')

    a1.plot(t,data_h_lm_real[0,:], label='real_initial_parameter', color='red', linewidth='0.8')
    a1.set_xlim((-200,50))
    a1.set_ylim((y_min,y_max))
    a1.set_xlabel("Time (M)")
    a1.grid(axis='x')
    #-----------------------------------------------------------------------------------------------------------------------------

    a2.plot(t,data_h_lm_imag[0,:], label='imag_initial_parameter', color='red', linewidth='0.8')
    a2.set_xlim((t[0],t[-1]))
    a2.set_ylim((y_min,y_max))  
    a2.set_xlabel("Time (M)")
    a2.set_ylabel(r"$\Im(h_{" + str(l) + str(m) + "})$")
    a2.grid(axis='x')

    a3.plot(t,data_h_lm_imag[0,:], label='imag_initial_parameter', color='red', linewidth='0.8')
    a3.set_xlim((-200,50))
    a3.set_ylim((y_min,y_max))
    a3.set_xlabel("Time (M)")
    a3.grid(axis='x')

    #-----------------------------------------------------------------------------------------------------------------------------
    a4.plot(t,data_h_abs[0,:], label='abs_initial_parameter', color='red', linewidth='0.8')
    a4.set_xlim((t[0],t[-1]))
    a4.set_ylim((0.,y_max))   
    a4.set_xlabel("Time (M)")
    a4.set_ylabel(r"$ \mid h_{" + str(l) + str(m) + "}\mid $")
    a4.grid(axis='x')

    a5.plot(t,data_h_abs[0,:], label='abs_initial_parameter', color='red', linewidth='0.8')
    a5.set_xlim((-200,50))
    a5.set_ylim((0.,y_max))
    a5.set_xlabel("Time (M)")
    a5.grid(axis='x')

    plot_title = plt.suptitle(r"$h_{" + str(l) + str(m) + "}$" + f" for {choose_parameter_to_vary} = {varying_param_values[0]:.2f} \n \n", fontsize=28, color='black')
    
    initial_param_text = f.text(0.19, 0.885,  f"Initial    -----> q = {all_parameter_values[0,0]:.2f}, chiA = ({all_parameter_values[0,1]:.2f} ,{all_parameter_values[0,2]:.2f} ,{all_parameter_values[0,3]:.2f}), chiB = ({all_parameter_values[0,4]:.2f} ,{all_parameter_values[0,5]:.2f} ,{all_parameter_values[0,6]:.2f})",ha="left", va="center", fontsize=18, color='red')
    final_param_text   = f.text(0.19, 0.845 ,  f"Current -----> q = {  all_parameter_values[0,0]:.2f}, chiA = ({all_parameter_values[0,1]:.2f} ,{all_parameter_values[0,2]:.2f} ,{all_parameter_values[0,3]:.2f}), chiB = ({all_parameter_values[0,4]:.2f} ,{all_parameter_values[0,5]:.2f} ,{all_parameter_values[0,6]:.2f})",ha="left", va="center", fontsize=18, color='#1f77b4')
        
    # Plot and store the line objects
    line0, = a0.plot(t, data_h_lm_real[0, :], label='Current_parameter')
    line1, = a1.plot(t, data_h_lm_real[0, :] )
    line2, = a2.plot(t, data_h_lm_imag[0, :])
    line3, = a3.plot(t, data_h_lm_imag[0, :])
    line4, = a4.plot(t, data_h_abs[0, :]  )
    line5, = a5.plot(t, data_h_abs[0, :]  )

    a0.legend(loc='upper left')
    f.tight_layout()

    def update(frame):
        # Update the data for each line object
        line0.set_ydata(data_h_lm_real[frame, :])
        line1.set_ydata(data_h_lm_real[frame, :])
        line2.set_ydata(data_h_lm_imag[frame, :])
        line3.set_ydata(data_h_lm_imag[frame, :])
        line4.set_ydata(data_h_abs[frame, :])
        line5.set_ydata(data_h_abs[frame, :])
        
        plot_title.set_text(r"$h_{" + str(l) + str(m) + "}$" + f" for {choose_parameter_to_vary} = {varying_param_values[frame]:.2f} \n \n")
        final_param_text.set_text(f"Current -----> q = {  all_parameter_values[frame,0]:.2f}, chiA = ({all_parameter_values[frame,1]:.2f} ,{all_parameter_values[frame,2]:.2f} ,{all_parameter_values[frame,3]:.2f}), chiB = ({all_parameter_values[frame,4]:.2f} ,{all_parameter_values[frame,5]:.2f} ,{all_parameter_values[frame,6]:.2f})")
               
        return [line0, line1, line2, line3, line4, line5, plot_title,final_param_text ]

    ani = FuncAnimation(f, update, frames=data_h_lm_real.shape[0], blit=False)

    FFMpegWriter = writers['ffmpeg']
    writer = FFMpegWriter(fps=video_fps, metadata=dict(artist='Akshay Khadse'), bitrate=10000)
    
    video_filepath = os.getcwd()+'/downloaded_videos/'+video_name
    ani.save(video_filepath, writer=writer)

    runtime = time.time()-start_time
    runtime = str(timedelta(seconds = runtime))
    print("==========================================================")
    print("Video Downloaded in : ",runtime)
    print("==========================================================")
    return generate_presigned_url(video_name)
