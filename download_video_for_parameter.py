import gwsurrogate
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import time

from utils import generate_video_for_varying_param

# User input parameters
q     = 1
chiAx = 0.
chiAy = 0.
chiAz = 0.
chiBx = 0.
chiBy = 0.
chiBz = 0.

choose_parameter_to_vary     = 'q'     # Choose from 'q', 'chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz'
parameter_start_value        = 1.
parameter_end_value          = 6.
parameter_steps              = 1*10 # performs at around 5 steps/second

l=2
m=2

user_input = {"q":q, 
              "chiAx":chiAx, "chiAy":chiAy, "chiAz":chiAz, 
              "chiBx":chiBx, "chiBy":chiBy, "chiBz":chiBz, 
              "choose_parameter_to_vary":choose_parameter_to_vary, 
              "parameter_start_value":parameter_start_value, "parameter_end_value":parameter_end_value, 
              "parameter_steps":parameter_steps, "l":l, "m":m}
#___________________________________________________________________________________________________________________________________


# Surrogate parameters
f_low = 0
times = np.arange(-4299,99,0.1)
sur   = gwsurrogate.LoadSurrogate('NRSur7dq4')


surrogate_params = {"sur":sur, "f_low":f_low, "times":times }
#___________________________________________________________________________________________________________________________________


# Video settings parameter
video_width  = 1500
video_height = 700
video_fps    = 24.0
video_name   = "h_lm_video.mp4"

video_params = {"video_width":video_width, "video_height":video_height, "video_fps":video_fps, "video_name":video_name }
#___________________________________________________________________________________________________________________________________


# Figure params
figsize       = (15,7)
figure_params = {"figsize":figsize}
#___________________________________________________________________________________________________________________________________


# Other params
allowed_params_to_vary = ['q','chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz']
other_params           = {"allowed_params_to_vary":allowed_params_to_vary}

########################################################################################################################################
########################################################################################################################################

# Combined final input to the code, everything below this will use this common object
input_dict = {"user_input":user_input, "surrogate_params":surrogate_params, "video_params":video_params,"figure_params":figure_params, "other_params":other_params}

########################################################################################################################################
########################################################################################################################################

if __name__=='__main__':
    start_time = time.time()

    generate_video_for_varying_param(input_dict)

    end_time = time.time()
    total_runtime_seconds = end_time - start_time
    minutes = int(total_runtime_seconds // 60)
    seconds = int(total_runtime_seconds % 60)

    print("Total runtime:", minutes, "minutes", seconds, "seconds")