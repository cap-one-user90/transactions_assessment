# Capital One Transactions Assessment

This is the data science assessment for Capitol One

## Results
Results can be found in the ```notebooks/Transactions Questions.ipynb``` notebook

## How to Use
There are a couple of different ways to use this package.

#### Use pip to install the package locally (this is probably the easiest way):
1. Install/activate ```python 3.9.0``` (This has been tested with ```3.8.8``` and should work with any version above ```3.7``` but no garantees)
2. Navigate to the project directory and run ```pip  setup.py install```
    - or you can install directly from github: ```pip install git+https://github.com/cap-one-user90/transactions_assessment.git```
3. Open up a ```jupyter notebook``` and open the ```Transaction Questions.ipynb``` notebook.
4. If this package is installed correctly, you should be able to run all the cells in that notebook

* You can also test out the package from the command line (after installing) by running:\
 ```transactions_assessment train-model --limit 100000``` (or use ```transactions_ssessment train-model``` to use all of the data

#### Run package interactively from virtualenv
Pre-reqs: ```pyenv >= 1.2.23```
You can re-create this virtual-environment by using the following steps:
From the project directory run:
1. ```$ make init```
2. ```$ make build```
3. ```$ make setup-jupyter```
4. ```$ make notebook``` (opens jupyter in browswer window -go to ```localhost:8888``` if not automatically directed)
* if any of these steps return an error, you can enter the commands found in the ```Makefile``` in this project manually



