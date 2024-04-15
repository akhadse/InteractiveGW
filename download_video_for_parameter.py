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
parameter_steps              = 1*24 # takes around 17.6 seconds to generate 1 second of video at 24fps (0.7 sec per parameter step)

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
delta_t = 1
sur_name = "NRSur7dq4"


surrogate_params = {"sur_name":sur_name, "f_low":f_low, "delta_t":delta_t }
#___________________________________________________________________________________________________________________________________


# Video settings parameters
video_width  = 1500
video_height = 700
video_fps    = 24.0
video_name   = "h_lm_video.mp4"

video_params = {"video_width":video_width, "video_height":video_height, "video_fps":video_fps, "video_name":video_name }
#___________________________________________________________________________________________________________________________________


# Figure settings parameters
figure_width  = 15
figure_height = 7
figure_params = {"figure_width":figure_width, "figure_height":figure_height}
#___________________________________________________________________________________________________________________________________


# Other params

other_params           = {}

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