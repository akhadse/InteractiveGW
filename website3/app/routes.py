from flask import Blueprint, render_template, request, redirect, url_for

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')