# cmpsc445-api
Flask based API that returns historic data for a given security, and LSTM predictin forecast for that security

# Important
The use of the API assumes that the model repository is installed in the same parent directory as the API. Connects to the test.db 
file under data folder.

# Enviroment 
A virtual enviroment would be recommend for this project utilzing python 3.8.10

For conda: 

```
conda create --name ENV_NAME pip python=3.8.10
conda activate ENV_NAME
pip install -r requirements.txt

conda deactivate
```

For pipenv:
```
pip install pipenv
pipenv install --python 3.8.10
pipenv shell
pip install -r requirements.txt

exit
```

Capturing requirements:
```
pip freeze > requiremts.txt
```