# Bulk Mail Sender

This Python project is designed to send bulk emails to a list of recipients using multiple email accounts configured through environment variables. The script is flexible and supports sending emails with attachments from different email providers.

## Project Structure
```
.
├── README.md
├── data
│        ├── attachment.pdf
│        ├── body.html
│        ├── body.txt
│        ├── recipients.txt
│        └── subject.txt
├── email_log.log
├── main.py
├── requirements.txt
└── src
    ├── __pycache__
    │        └── bulk_mail.cpython-312.pyc
    └── bulk_mail.py
```

## Setup and Installation

	1.	Clone the repository:
```bash
git clone https://github.com/your_username/bulk_mail_sender.git
cd bulk_mail_sender
```

	2.	Install dependencies:
```bash
pip install -r requirements.txt
```

	3.	Configure Environment Variables:
	•	Rename .env.example to .env.
	•	Add your email account details to .env. Multiple accounts can be configured; simply specify account names in the EMAIL_ACCOUNTS list as follows:

EMAIL_ACCOUNTS=["EMAIL1", "EMAIL2", "EMAIL3"]

EMAIL1_EMAIL=your_email@example.com
EMAIL1_PASSWORD=your_password
EMAIL1_SMTP_SERVER=smtp.example.com
EMAIL1_SMTP_PORT=465
EMAIL1_SMTP_SSL=True

EMAIL2_EMAIL=your_gmail@example.com
EMAIL2_APP_PASSWORD=your_gmail_app_password


	4.	Set up Email Data Files:
	•	Place the following files in the data folder:
	•	recipients.txt - list of recipients separated by commas, semicolons, or line breaks.
	•	subject.txt - contains the email subject.
	•	body.html or body.txt - contains the email body (HTML or plain text).
	•	Additional attachments can be added as files in the data folder.

## Usage

The script can be executed from the command line or by running main.py. Here’s an example of how to configure and send bulk emails:

	1.	Edit main.py to define:

email_account_name = "EMAIL1"          # Account defined in .env
recipients_filename = "recipients.txt" # Recipient list file in data/
subject_filename = "subject.txt"       # Subject file in data/
body_filename = "body.html"            # Email body file in data/
attachments = ["attachment.pdf"]       # List of attachment filenames in data/


	2.	Run the script:
```bash
python main.py
```


Functionality

	•	Account Management: Loads multiple email accounts from .env, allowing you to switch between them.
	•	Bulk Emailing: Reads recipients, subject, and body content from files and sends individual emails to each recipient.
	•	Attachment Support: Attach files located in the data folder.
	•	Error Handling: Logs errors if an email fails to send, such as issues connecting to SMTP servers or invalid recipient addresses.

Customization

	•	Update src/bulk_mail.py for additional customization, such as:
	•	Custom logging.
	•	Email formatting (e.g., HTML vs. plain text).
	•	Adjusting retry mechanisms for failed emails.

Dependencies

	•	yagmail - for email handling via SMTP.
	•	dotenv - to securely manage environment variables.

Install all dependencies with:
```bash
pip install -r requirements.txt
```
## Security

Ensure .env is added to .gitignore to avoid committing sensitive information to the repository. Always use application-specific passwords for Gmail accounts if enabled.

This README provides a clear and visually organized guide to setting up and running your bulk email sender script. Let me know if you want to add any other specific details!
