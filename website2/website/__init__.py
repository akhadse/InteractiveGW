from flask import Flask

def create_app():
    app = Flask(__name__)

    # import routes
    from .pages import pages

    # register routes
    app.register_blueprint(pages, url_prefix='/')

    return app