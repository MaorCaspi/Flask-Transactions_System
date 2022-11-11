import uuid,random, os
from flask import Flask, send_file
from flask_restful import reqparse
from datetime import date, timedelta
from pathlib import Path

DB_FOLDER_PATH = "daily transactions files"
REPORT_FILE_PATH = "report.txt"

app = Flask(__name__)

if not os.path.exists(DB_FOLDER_PATH):  
    # If the 'daily transactions files' folder isn't exists - then create it
    os.makedirs(DB_FOLDER_PATH)

def get_date(num_of_minus_days):
	"""
	Return (date of today's date - 'num_of_minus_days') in a format like 30-01-2022
    """
	return str((date.today()- timedelta(days = num_of_minus_days)).strftime("%d-%m-%Y"))

def get_daily_transactions_file_path(num_of_minus_days):
	"""
	Return the daily transactions file path of (today's date - 'num_of_minus_days')
	For example - daily transactions files\\30-01-2022.txt
	"""
	return Path(DB_FOLDER_PATH + "\\"+get_date(num_of_minus_days) + ".txt")


@app.route('/', methods=['GET'])
def download_report():
	"""
	Downloads a daily report of transaction results.	
	It may contain info about transactions from the last 5 days.
	The report format is:
	transaction_id, success/fail
	"""
	return_data = ""
	for i in range (4 ,-1, -1):
		file_path = get_daily_transactions_file_path(i)
		if file_path.is_file():
			with open(file_path, "r") as f:
				return_data += f.read()
				return_data += "\n"
	with open (REPORT_FILE_PATH, 'w') as f:
		f.write(return_data)

	return send_file(REPORT_FILE_PATH, as_attachment=True)

@app.route('/', methods=['POST'])
def perform_transaction():
	"""
	Perform a transaction.	
	This call returns the new transaction_id after the creation.
	"""
	parser = reqparse.RequestParser() # Validate body parames
	parser.add_argument("src_bank_account", type=str, help="src_bank_account is required", required=True)
	parser.add_argument("dst_bank_account", type=str, help="dst_bank_account is required", required=True)
	parser.add_argument("amount", type=float, help="amount is required", required=True)
	parser.add_argument("direction", choices=('credit', 'debit'), help="direction is required", required=True)

	args = parser.parse_args()
	print("New transaction from: " + args['src_bank_account'] + " to: " + args['dst_bank_account'] + " the amount is: " + str(args['amount']))
		
	if args["direction"] == "debit":
		rnd_num=random.randint(0,9) # Simulate success/fail transaction_status using random
		if(rnd_num <= 7):
			transaction_status = "success"
		else:
			transaction_status = "fail"
	else: # Credit status is always successful
		transaction_status = "success"

	transaction_id = str(uuid.uuid4())

	file_path = get_daily_transactions_file_path(0) # Get the transactions file path of today's transactions
	if not file_path.is_file():
		f = open(file_path, "w")
		f.write("# Transactions of " + get_date(0) + " #")
	else:
		f = open(file_path, "a")
	f.write("\n" + transaction_id + "," + transaction_status)
	f.close()
	return(transaction_id, 200)

if __name__ == "__main__":
	app.run(debug = False, port = 5000)