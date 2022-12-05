# OCR_DAP_P4
Développeur d'Application Python - Projet 4



## Setup

### Directory setup
It is recommended to create a dedicated directory to download the project.
In a terminal:
`mkdir dir_name`

### Git setup
Initialize your local Git repository. In a terminal (in your dedicated directory):
`git init`

Then clone the remote repository in your local repository with the https link. You will find the https link is in the "code" drop-down menu:
`git clone https_project_link`

### Virtual environment setup
Set a virtual environment before installing the dependencies:
`python3.9 -m venv env`

To activate your virtual environment:
`source env/bin/activate`

Then, you can install the python dependencies for the project: 
`pip install -r requirements.txt`


## Launch the program

From the root directory launch the program:
`python ./main.py`


## Flake8 report 

From the root directory generate a new Flake8 report:
`flake8 ./ --format=html --htmldir=flake8_rapport`

You can generate fake data (1 fake tournament and 1 fake player) with the file `fake_data.py`
You can empty the data base with the file `reset_db.py`