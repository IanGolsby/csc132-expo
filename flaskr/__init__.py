import os
import values, random
#import sensor_testing as sTest # might need to be moved outside of folder, similar to values module
from flask import Flask, render_template, request


def buttonPress(val):
    return not val

def names():
    """
    lists = ["helium", "fart", "mustard", "cs2", "c2o", "co"]
    name = random.choice(lists)
    """
    #name = sTest.detected # gets name of what is detected\
    with open('detected.txt') as f:
        name = f.read()
    return name    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    # home page that shows what is detected
    @app.route('/')
    def server():
        """
        if values.value == False:
            return render_template('hello1.html', name=names())
        elif values.value == True:
            return render_template('hello1.html', name=names()) # originially to be html1
        """
        return render_template("hello1.html")

    # a page that has a button that manipulates the boolean values.value
    # in order to switch /server background color
    @app.route('/pi', methods=['GET', 'POST'])
    def pi():
        """
        if request.method == 'POST':
            if request.form['submit_button'] == 'Click Me' and values.value == False:
                values.value = True

            elif request.form['submit_button'] == 'Click Me' and values.value == True:
                values.value = False
        """
        return render_template("piSide.html", name=values.value)

    return app