import os
from flask import Flask, render_template


def names():
    """Returns string located in detected.txt"""

    with open('detected.txt') as f:
        name = f.read()
    return name    


def create_app(test_config=None):
    """create and configure the app"""

    app = Flask(__name__, instance_relative_config=True)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.static_folder = 'static'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/')
    def server():
        """home page that shows what is detected"""

        return render_template("hello1.html")


    @app.route('/pi', methods=['GET', 'POST'])
    def pi():
        """/pi page"""

        return render_template("piSide.html", name=names())

    @app.route('/iframe')
    def iframes():
        """Page for iframe that is located in /pi"""
        return render_template("iframe.html", name=names())

    return app