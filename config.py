import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database 
SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False