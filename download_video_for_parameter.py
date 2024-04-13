import gwsurrogate
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import cv2

sur   = gwsurrogate.LoadSurrogate('NRSur7dq4')

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
parameter_steps              = 24*10 # performs at around 5 steps/second

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

surrogate_params = {"f_low":f_low, "times":times}
#___________________________________________________________________________________________________________________________________


# Video settings parameter
video_params = {""}
#___________________________________________________________________________________________________________________________________


########################################################################################################################################
########################################################################################################################################

# Combined final input to the code, everything below this will use this common object
input_dict = {"user_input":user_input, "surrogate_params":surrogate_params, "video_params":video_params}

########################################################################################################################################
########################################################################################################################################


user_input = input_dict["user_input"]
surrogate_params = input_dict["surrogate_params"]
video_params = input_dict["video_params"]

q     = user_input[""]
chiAx = 0.
chiAy = 0.
chiAz = 0.
chiBx = 0.
chiBy = 0.
chiBz = 0.

choose_parameter_to_vary     = 'q'     # Choose from 'q', 'chiAx', 'chiAy', 'chiAz', 'chiBx', 'chiBy', 'chiBz'
parameter_start_value        = 1.
parameter_end_value          = 6.
parameter_steps              = 24*10 # performs at around 5 steps/second

l=2
m=2


