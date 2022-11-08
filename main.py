import uuid,random, os
from flask import Flask, send_file
from flask_restful import Api, Resource, reqparse
from datetime import date, timedelta
from pathlib import Path

app = Flask(__name__)
api = Api(app)

if not os.path.exists("daily transactions files"):  
    # If the 'daily transactions files' folder isn't exists - then create it
    os.makedirs("daily transactions files")

processor_args = reqparse.RequestParser() # Validate body parames of any post req
processor_args.add_argument("src_bank_account", type=str, help="src_bank_account is required", required=True)
processor_args.add_argument("dst_bank_account", type=str, help="dst_bank_account is required", required=True)
processor_args.add_argument("amount", type=float, help="amount is required", required=True)
processor_args.add_argument("direction", choices=('credit', 'debit'), help="direction is required", required=True)

def get_date(num_of_minus_days):
	'''
	Return (date of today's date - 'num_of_minus_days') in a format like 30-01-2022
    '''
	return str((date.today()- timedelta(days = num_of_minus_days)).strftime("%d-%m-%Y"))

def get_daily_transactions_file_path(num_of_minus_days):
	'''
	Return the daily transactions file path of (today's date - 'num_of_minus_days')
	:For example - daily transactions files\\30-01-2022.txt
	'''
	return Path("daily transactions files\\"+get_date(num_of_minus_days) + ".txt")

class Processor(Resource):

	def get(self):
		return_data = ""
		for i in range (4 ,-1, -1):
			file_path = get_daily_transactions_file_path(i)
			if file_path.is_file():
				with open(file_path, "r") as f:
					return_data += f.read()
					return_data += "\n"
		print(return_data)
		with open ('report.txt', 'w') as f:
			f.write(return_data)

		return send_file("report.txt", as_attachment=True)

	
	def post(self):
		args = processor_args.parse_args()
		print("New transaction from: " + args['src_bank_account'] + " to: " + args['dst_bank_account'] + " the amount is: " + str(args['amount']))
		
		rnd_num=random.randint(0,9) # Simulate success/fail transaction_status using random
		if(rnd_num <= 7):
			transaction_status="success"
		else:
			transaction_status="fail"

		transaction_id = str(uuid.uuid4())

		file_path = get_daily_transactions_file_path(0)
		if not file_path.is_file():
			f = open(file_path, "w")
			f.write("# Transactions of " + get_date(0) + " #")
		else:
			f = open(file_path, "a")
		f.write("\n" + transaction_id + "," + transaction_status)
		f.close()
		return(transaction_id, 200)

api.add_resource(Processor, "/")

if __name__ == "__main__":
	app.run(debug=True)