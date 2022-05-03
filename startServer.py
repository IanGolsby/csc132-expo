import subprocess

directory = "/Documents/Programming/RPi_Proj"




# runs the flask server
subprocess.run("export FLASK_APP=flaskr && export FLASK_ENV=development && flask run", shell=True)
#subprocess.run('export FLASK_ENV=development', shell=True)
#subprocess.run('flask run', shell=True)



