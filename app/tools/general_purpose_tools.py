import csv, re

def csv_export(csv_name, rows, keys):  
    ''' 
    Export csv with column names specified by the keys list
    and column contents specified by the rows dict. 
    '''  
    with open(csv_name, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for row in rows:
            dict_writer.writerow(row)

def validate_email(email, name=""):
    ''' 
    Ensure the given email is an actual email using regular expressions. 
    '''  
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print(name, 'Bad email. Please re-enter email.')
        raise
   