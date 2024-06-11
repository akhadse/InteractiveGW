from flask import Flask


def create_app():
    app = Flask(__name__)

    # import routes
    from .routes import routes

    # register routes
    app.register_blueprint(routes, url_prefix='/')

    return app