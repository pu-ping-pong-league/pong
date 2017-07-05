# pong - MVP version
Interface for Managing the Princeton University Ping Pong League

Dependencies: virtualenv, mysql, python 2.7

MySQL username: web2pyuser
/ MySQL password: password

Setup and first execution:

    Setup virtual environment:
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    
    Start mysql and create pong database:
    $ sudo service mysql start
    $ mysql -u <username> -p <password>
      > create database pong;
      > exit
      
    Define the database tables and run the Pong Interface:
    $ python initialize.py
    
Run the pong interface assuming setup has been performed:

    Activate virtual environment:
    $ source venv/bin/activate
    
    Start mysql:
    $ sudo service mysql start
      
    Run the Pong Interface:
    $ python run.py


    
    
    
