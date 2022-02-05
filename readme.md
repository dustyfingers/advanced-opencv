windows setup for each project:

navigate to the project's root dir and run the following (must use python 3.6 so replace the fp below with the location of your local python 3.6 installation):
virtualenv .  -p C:/Users/PC/AppData/Local/Programs/Python/Python36/python.exe

to activate the virtual env: 
./Scripts/activate

to deactivate just run:
deactivate

to start a new virtual env in a project contained here (for me lol): navigate to new project dir && run --> virtualenv .  -p C:/Users/PC/AppData/Local/Programs/Python/Python36/python.exe

macos setup:
to set up the virtual env, navigate to the root dir of the project you are working on and run:
virtualenv venv

if you want your virtualenv to inherit globally installed packages, run:
virtualenv venv --system-site-packages

to run the virtualenv, run:
source venv/bin/activate

to leave the virtual env, run:
deactivate