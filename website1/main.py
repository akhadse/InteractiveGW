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

        form_data["choose_parameter_to_vary"] = str(form_data["choose_parameter_to_vary"])
        form_data["parameter_start_value"] = float(form_data["parameter_start_value"])
        form_data["parameter_end_value"] = float(form_data["parameter_end_value"])
        form_data["parameter_steps"] = float(form_data["parameter_steps"])
        form_data["l"] = int(form_data["l"])
        form_data["m"] = int(form_data["m"])

        form_data["q"] = float(form_data["q"])
        form_data["chiAx"] = float(form_data["chiAx"])
        form_data["chiAy"] = float(form_data["chiAy"])
        form_data["chiAz"] = float(form_data["chiAz"])
        form_data["chiBx"] = float(form_data["chiBx"])
        form_data["chiBy"] = float(form_data["chiBy"])
        form_data["chiBz"] = float(form_data["chiBz"])

        form_data["f_low"] = float(form_data["f_low"])
        form_data["delta_t"] = float(form_data["delta_t"])
        form_data["sur_name"] = str(form_data["sur_name"])

        form_data["video_width"] = float(form_data["video_width"])
        form_data["video_height"] = float(form_data["video_height"])
        form_data["video_fps"] = float(form_data["video_fps"])
        form_data["video_name"] = str(form_data["video_name"])

        form_data["figure_width"] = float(form_data["figure_width"])
        form_data["figure_height"] = float(form_data["figure_height"])
        
        output = generate_video_for_varying_param(form_data)
        return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
