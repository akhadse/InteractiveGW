from flask import Flask, render_template, request
from function import *
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        parameter = request.form['parameter']
        output = square_the_number(parameter)
        return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
