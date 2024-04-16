from flask import Flask, render_template, request
from function import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':     

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
        return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
