# bulk_mail.py
import os

import yagmail
from dotenv import load_dotenv


def load_accounts():
    accounts = {}
    load_dotenv()
    account_names = eval(os.getenv('EMAIL_ACCOUNTS'))
    for name in account_names:
        email = os.getenv(f'{name.upper()}_EMAIL')
        password = os.getenv(f'{name.upper()}_APP_PASSWORD') or os.getenv(f'{name.upper()}_PASSWORD')
        smtp_server = os.getenv(f'{name.upper()}_SMTP_SERVER')
        smtp_port = os.getenv(f'{name.upper()}_SMTP_PORT')
        smtp_ssl = os.getenv(f'{name.upper()}_SMTP_SSL', 'True') == 'True'
        accounts[name] = {
            'name': name,
            'email': email,
            'password': password,
            'smtp_server': smtp_server,
            'smtp_port': int(smtp_port) if smtp_port else None,
            'smtp_ssl': smtp_ssl
        }
    return accounts


def get_recipients(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        # Split emails by comma, semicolon, or newline
        recipients = [email.strip() for email in data.replace('\n', ',').replace(';', ',').split(',') if email.strip()]
    return recipients


def get_email_content(subject_path, body_path):
    # Read subject from file
    with open(subject_path, 'r') as file:
        subject = file.read().strip()
    # Read body from file
    with open(body_path, 'r') as file:
        body = file.read()
    return subject, body


def send_emails(account, recipients, subject, body, attachments, data_folder):
    try:
        if 'gmail' in account['email'].lower():
            yag = yagmail.SMTP(account['email'], account['password'])
        else:
            yag = yagmail.SMTP(
                user=account['email'],
                password=account['password'],
                host=account['smtp_server'],
                port=account['smtp_port'],
                smtp_ssl=account['smtp_ssl']
            )
    except Exception as e:
        print(f"Failed to connect to SMTP server: {e}")
        return

    # Prepend data_folder to attachment paths
    attachment_paths = [os.path.join(data_folder, attachment) for attachment in attachments]

    for recipient in recipients:
        try:
            yag.send(
                to=recipient,
                subject=subject,
                contents=[body],
                attachments=attachment_paths
            )
            print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")


def send_bulk_emails(account_name, recipients_filename, subject_filename, body_filename, attachment_filenames):
    # Load accounts
    accounts = load_accounts()
    if account_name not in accounts:
        print(f"Account '{account_name}' not found.")
        return
    account = accounts[account_name]

    # Set paths
    data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    recipients_file = os.path.join(data_folder, recipients_filename)
    subject_file = os.path.join(data_folder, subject_filename)
    body_file = os.path.join(data_folder, body_filename)

    # Get recipients, subject, body
    recipients = get_recipients(recipients_file)
    subject, body = get_email_content(subject_file, body_file)

    # Send emails
    send_emails(account, recipients, subject, body, attachment_filenames, data_folder)
