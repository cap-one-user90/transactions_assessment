# Capital One Transactions Assessment

This is the data science assessment for Capitol One

## Results
Results can be found in the ```notebooks/Transactions Questions.ipynb``` notebook

## How to Use
There are a couple of different ways to use this package.\

#### Use ```pip ``` to install the package locally (this is probably the easiest way):
1. Install/activate ```python 3.9.0```
2. Navigate to the project directory and run ```pip  setup.py install```
3. Open up a ```jupyter notebook``` and open the ```Transaction Questions.ipynb``` notebook.
4. If this package is installed correctly, you should be able to run all the cells in that notebook

#### Run package interactively from virtualenv
Pre-reqs: ```pyenv >= 1.2.23```\
You can re-create this virtual-environment by using the following steps:\
From the project directory run:\
 1. ```$ make init```\
 2.```$ make build```\
 3. ```$ make setup-jupyter```\
 4. ```$ make notebook``` (opens jupyter in browswer window -go to ```localhost:8888``` if not automatically directed)
 * if any of these steps return an error, you can enter the commands found in the ```Makefile``` in this project manually



