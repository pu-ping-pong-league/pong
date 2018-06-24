# pong
Interface for managing the Princeton University Ping Pong League. **Dependencies:** virtualenv, mysql, python 2.7.

## Setup and first execution:
1. Adjust `config.py` file based on your preferences and include your personal credentials.
2. Setup virtual environment:
```
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```   
3. Start mysql and create pong database:
```
    $ sudo service mysql start
    $ mysql -u <username> -p <password>
      > create database pong;
      > exit;
```
4. Define the database tables and run the Pong Interface:
```
    $ python initialize.py
```
    
## Load the pong interface given successful setup:
1. Activate virtual environment:
```
    $ source venv/bin/activate
```
2. Start mysql:
```
    $ sudo service mysql start
```
3. Run the Pong Interface:
```
    $ python run.py
```


    
    
    
