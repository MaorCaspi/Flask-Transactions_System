## Flask-Transactions_System
### Intrudaction
Rest API for money transfers between banks.<br/>

### Supports two calls:
1 - perform_transaction (src_bank_account, dst_bank_account, amount, direction) -(a POST reuest)<br/>
direction = credit / debit<br/>
This call perform new transaction and return the new transaction_id<br/><br/>
2 - download_report () -(a GET request)<br/>
This downloads a daily report of transaction results.<br/>
The file contain info about transactions from the last 5 days.<br/>
The report format is:<br/>
transaction_id, success/fail<br/>

### Notes
This server has default port number 5000<br/>
To run the server please install all the libraries at the requirements.txt file, and then run the file main.py<br/>
This API is used in a separate API project "Flask-Billing_System" a system that send requests to this API and uses it.

### Links
Documentation page:<br/>
https://documenter.getpostman.com/view/20844564/2s8YeptYRb<br/><br/>
Flask-Billing_System:<br/>
https://github.com/MaorCaspi/Flask-Billing_System<br/><br/>

Author: Maor Caspi<br/>
Date: December 2022
