import os
import sys
import yagmail
from dotenv import load_dotenv


def load_accounts():
    accounts = []
    load_dotenv()
    account_names = eval(os.getenv('EMAIL_ACCOUNTS'))
    for name in account_names:
        email = os.getenv(f'{name.upper()}_EMAIL')
        password = os.getenv(f'{name.upper()}_APP_PASSWORD') or os.getenv(f'{name.upper()}_PASSWORD')
        accounts.append({'name': name, 'email': email, 'password': password})
    return accounts


def select_account(accounts):
    print("Select the email account to send from:")
    for idx, account in enumerate(accounts):
        print(f"{idx + 1}. {account['name']} ({account['email']})")
    choice = int(input("Enter the number of your choice: ")) - 1
    return accounts[choice]


def get_recipients(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        # Split emails by semicolon or newline
        recipients = [email.strip() for email in data.replace('\n', ';').split(';') if email.strip()]
    return recipients


def get_email_content(subject_path, body_path):
    # Read subject from file
    with open(subject_path, 'r') as file:
        subject = file.read().strip()
    # Read body from file
    with open(body_path, 'r') as file:
        body = file.read()
    return subject, body


def get_attachments(data_folder):
    attachments = []
    for filename in os.listdir(data_folder):
        if filename.startswith('attachment'):
            attachments.append(os.path.join(data_folder, filename))
    return attachments


def send_emails(account, recipients, subject, body, attachments):
    yag = yagmail.SMTP(account['email'], account['password'])
    for recipient in recipients:
        try:
            yag.send(
                to=recipient,
                subject=subject,
                contents=[body],
                attachments=attachments
            )
            print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")


def main():
    # Set paths
    data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    recipients_file = os.path.join(data_folder, 'recipients.txt')
    subject_file = os.path.join(data_folder, 'subject.txt')
    body_file = os.path.join(data_folder, 'body.txt')

    # Load accounts and select one
    accounts = load_accounts()
    account = select_account(accounts)

    # Get recipients, subject, body, and attachments
    recipients = get_recipients(recipients_file)
    subject, body = get_email_content(subject_file, body_file)
    attachments = get_attachments(data_folder)

    # Send emails
    send_emails(account, recipients, subject, body, attachments)


if __name__ == "__main__":
    main()