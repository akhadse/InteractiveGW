from flask import Blueprint, render_template, request, redirect, url_for

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')


@routes.route('/interactive_strain', methods=['GET', 'POST'])
def interactive_strain():
    return render_template('interactive_strain.html')

@routes.route('/interactive_h_lm', methods=['GET', 'POST'])
def interactive_h_lm():
    return render_template('interactive_h_lm.html')

@routes.route('/download_videos', methods=['GET', 'POST'])
def download_videos():
    return render_template('download_videos.html')
