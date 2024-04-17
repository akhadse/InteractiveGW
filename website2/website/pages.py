from flask import Blueprint, render_template, request
from .utils import generate_video_for_varying_param

pages = Blueprint('pages', __name__)

@pages.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')


@pages.route('/download_GW', methods=['GET', 'POST'])
def download_GW():

    if request.method == 'POST':
        print("=================")
        print("Started making video -----")
        print("=================")      
        
        form_data = request.form.to_dict()

        choose_parameter_to_vary = str(form_data["choose_parameter_to_vary"])
        parameter_start_value = float(form_data["parameter_start_value"])
        parameter_end_value = float(form_data["parameter_end_value"])
        parameter_steps = int(form_data["parameter_steps"])
        l = int(form_data["l"])
        m = int(form_data["m"])

        q = float(form_data["q"])
        chiAx = float(form_data["chiAx"])
        chiAy = float(form_data["chiAy"])
        chiAz = float(form_data["chiAz"])
        chiBx = float(form_data["chiBx"])
        chiBy = float(form_data["chiBy"])
        chiBz = float(form_data["chiBz"])

        f_low = float(form_data["f_low"])
        delta_t = float(form_data["delta_t"])
        sur_name = str(form_data["sur_name"])

        video_width = int(form_data["video_width"])
        video_height = int(form_data["video_height"])
        video_fps = float(form_data["video_fps"])
        video_name = str(form_data["video_name"])

        figure_width = float(form_data["figure_width"])
        figure_height = float(form_data["figure_height"])


        user_input = {"q":q, 
              "chiAx":chiAx, "chiAy":chiAy, "chiAz":chiAz, 
              "chiBx":chiBx, "chiBy":chiBy, "chiBz":chiBz, 
              "choose_parameter_to_vary":choose_parameter_to_vary, 
              "parameter_start_value":parameter_start_value, "parameter_end_value":parameter_end_value, 
              "parameter_steps":parameter_steps, "l":l, "m":m}
        surrogate_params = {"sur_name":sur_name, "f_low":f_low, "delta_t":delta_t }
        video_params = {"video_width":video_width, "video_height":video_height, "video_fps":video_fps, "video_name":video_name }
        figure_params = {"figure_width":figure_width, "figure_height":figure_height}
        input_dict = {"user_input":user_input, "surrogate_params":surrogate_params, "video_params":video_params,"figure_params":figure_params}
        
        output = generate_video_for_varying_param(input_dict)
        print("=================")
        print("Done!!!")
        print("=================")
        return render_template('base.html')

    else:
        return render_template('download_GW.html')
    


import numpy as np
from flask import jsonify

@pages.route('/interactive_GW', methods=['GET', 'POST'])
def interactive_GW():
    return render_template('interactive_GW.html')


@pages.route('/interactive_GW_update_route', methods=['POST'])
def interactive_GW_updating_function():
    parameter = request.form.get('parameter')

    if parameter is None:
        parameter = '5'
    parameter = float(parameter)
    x_values = np.arange(0, 10, 0.1)
    y_values = np.sin(parameter * x_values)
    x_values, y_values = x_values.tolist(), y_values.tolist()
    return jsonify({'x_values': x_values, 'y_values': y_values})