import os

# initialize database
os.system('rm -r migrations')
os.system('python manage.py db init')
os.system('python manage.py db migrate')
os.system('python manage.py db upgrade')

# run client
os.system('python run.py')