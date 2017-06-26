DEBUG = True
TESTING = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database 
SQLALCHEMY_DATABASE_URI ='mysql+pymysql://web2pyuser:password@localhost/pong'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False