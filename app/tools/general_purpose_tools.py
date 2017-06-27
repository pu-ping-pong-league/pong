import csv, re

def csv_export(csv_name, rows, keys):    
    with open(csv_name, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rows)

def validate_email(email, name=""):
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		print name, 'Bad email. Please re-enter email.'
		raise

   