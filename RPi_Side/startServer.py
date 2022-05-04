import subprocess

def refreshServer():
    subprocess.run("flask run")

# runs the flask server
subprocess.run("export FLASK_APP=flaskr && export FLASK_ENV=development && flask run", shell=True)




    

