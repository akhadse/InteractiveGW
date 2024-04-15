from flask import Flask, render_template, request
from function import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        choose_parameter_to_vary = request.form['choose_parameter_to_vary']
        parameter_start_value = request.form['parameter_start_value']
        parameter_end_value = request.form['parameter_end_value']
        parameter_steps = request.form['parameter_steps']
        l = request.form['l']
        m = request.form['m']
        q     = request.form['q']
        chiAx = request.form['chiAx']
        chiAy = request.form['chiAy']
        chiAz = request.form['chiAz']
        chiBx = request.form['chiBx']
        chiBy = request.form['chiBy']
        chiBz = request.form['chiBz']

        video_width  = request.form['video_width']
        video_height = request.form['video_height']
        video_fps    = request.form['video_fps']
        video_name   = request.form['video_name']

        video_params = {"video_width":video_width, "video_height":video_height, "video_fps":video_fps, "video_name":video_name }

        user_input = {"q":q, 
              "chiAx":chiAx, "chiAy":chiAy, "chiAz":chiAz, 
              "chiBx":chiBx, "chiBy":chiBy, "chiBz":chiBz, 
              "choose_parameter_to_vary":choose_parameter_to_vary, 
              "parameter_start_value":parameter_start_value, "parameter_end_value":parameter_end_value, 
              "parameter_steps":parameter_steps, "l":l, "m":m}

        output = generate_video(parameter)
        return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
