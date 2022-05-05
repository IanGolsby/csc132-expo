import os
from flask import Flask, render_template

def names():
    """Returns string located in detected.txt"""
    
    with open('detected.txt') as f:
        name = f.read()
    
    return name if name != "" else "EMPTY DATA RECEIVED"
    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance foler exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # server page
    @app.route('/')
    def home():
        return render_template("hq.html", name=names())

    @app.route('/iframe')
    def iframes():
        """Page for iframe that is located in /pi"""
        return render_template("iframe.html", name=names())

    return app
