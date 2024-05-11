from flask import Blueprint, render_template, request, redirect, url_for
from .utils.utils import *

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


@routes.route('/interactive_strain_update_route', methods=['POST'])
def interactive_strain_update_route():
    inclination = request.form.get('inclination')
    phi_ref     = request.form.get('phi_ref')
    q     = request.form.get('mass_ratio')
    chiAx = request.form.get('chiAx')
    chiAy = request.form.get('chiAy')
    chiAz = request.form.get('chiAz')
    chiBx = request.form.get('chiBx')
    chiBy = request.form.get('chiBy')
    chiBz = request.form.get('chiBz')

    if inclination is None: inclination=0
    if phi_ref      is None: phi_ref=0
    if q     is None: mass_ratio = 1.
    if chiAx is None: chiAx=0.
    if chiAy is None: chiAy=0.
    if chiAz is None: chiAz=0.
    if chiBx is None: chiBx=0.
    if chiBy is None: chiBy=0.
    if chiBz is None: chiBz=0.

    inclination = int(inclination)
    phi_ref      = int(phi_ref)
    q          = float(q)
    chiAx      = float(chiAx)
    chiAy      = float(chiAy)
    chiAz      = float(chiAz)
    chiBx      = float(chiBx)
    chiBy      = float(chiBy)
    chiBz      = float(chiBz)

    input_dict = {"q":q, "chiAx":chiAx, "chiAy":chiAy, "chiAz":chiAz, "chiBx":chiBx, "chiBy":chiBy, "chiBz":chiBz, "inclination":inclination, "phi_ref":phi_ref}

    return generate_strain_for_param(input_dict)


@routes.route('/interactive_h_lm_update_route', methods=['POST'])
def interactive_h_lm_updating_function():
    l = request.form.get('l')
    m = request.form.get('m')
    q = request.form.get('mass_ratio')
    chiAx = request.form.get('chiAx')
    chiAy = request.form.get('chiAy')
    chiAz = request.form.get('chiAz')
    chiBx = request.form.get('chiBx')
    chiBy = request.form.get('chiBy')
    chiBz = request.form.get('chiBz')

    if l is None: l=2
    if m is None: m=2
    if q is None: mass_ratio = 1.
    if chiAx is None: chiAx=0.
    if chiAy is None: chiAy=0.
    if chiAz is None: chiAz=0.
    if chiBx is None: chiBx=0.
    if chiBy is None: chiBy=0.
    if chiBz is None: chiBz=0.

    l = int(l)
    m = int(m)
    q = float(q)
    chiAx      = float(chiAx)
    chiAy      = float(chiAy)
    chiAz      = float(chiAz)
    chiBx      = float(chiBx)
    chiBy      = float(chiBy)
    chiBz      = float(chiBz)

    input_dict = {"q":q, "chiAx":chiAx, "chiAy":chiAy, "chiAz":chiAz, "chiBx":chiBx, "chiBy":chiBy, "chiBz":chiBz, "l":l, "m":m}

    return generate_sur_h_lm_for_param(input_dict)