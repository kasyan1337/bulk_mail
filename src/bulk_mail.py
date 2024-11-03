import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load email account details from environment variables
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

# Load recipients from a file
def get_recipients(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        recipients = [email.strip() for email in data.replace('\n', ',').replace(';', ',').split(',') if email.strip()]
    return recipients

# Load email subject and body content from files
def get_email_content(subject_path, body_path):
    with open(subject_path, 'r') as file:
        subject = file.read().strip()
    with open(body_path, 'r') as file:
        body = file.read()
    return subject, body

# Get file paths for any attachments
def get_attachment_paths(folder_path):
    if os.path.exists(folder_path):
        return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                os.path.isfile(os.path.join(folder_path, filename))]
    return []

# New send_emails_smtp function using smtplib and MIMEText
def send_emails_smtp(account, recipients, subject, body, attachment_paths, format_html):
    try:
        # Set up the SMTP server
        if 'gmail' in account['email'].lower():
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_ssl = False
        else:
            smtp_server = account['smtp_server']
            smtp_port = account['smtp_port']
            smtp_ssl = account['smtp_ssl']

        if smtp_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

        server.login(account['email'], account['password'])

        for recipient in recipients:
            # Set up the MIME message structure
            msg = MIMEMultipart('alternative')
            msg['From'] = account['email']
            msg['To'] = recipient
            msg['Subject'] = subject

            # Attach the HTML or plain text content
            if format_html:
                html_part = MIMEText(body, 'html')
                msg.attach(html_part)
            else:
                text_part = MIMEText(body, 'plain')
                msg.attach(text_part)

            # Attach any files
            if attachment_paths:
                for attachment_path in attachment_paths:
                    with open(attachment_path, 'rb') as f:
                        attachment = MIMEText(f.read(), 'base64', 'utf-8')
                        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                        msg.attach(attachment)

            # Send the email
            server.sendmail(account['email'], recipient, msg.as_string())
            print(f"Email sent to {recipient}")

        # Close the server connection
        server.quit()

    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function to initiate the bulk email sending process
def send_bulk_emails(account_name, recipients_filename, subject_filename, body_filename):
    accounts = load_accounts()
    if account_name not in accounts:
        print(f"Account '{account_name}' not found.")
        return
    account = accounts[account_name]

    # Define file paths for data
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email')
    attachments_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attachments')

    recipients_file = os.path.join(data_folder, recipients_filename)
    subject_file = os.path.join(data_folder, subject_filename)
    body_file = os.path.join(data_folder, body_filename)

    # Automatically determine format_html based on the body file extension
    format_html = body_filename.endswith('.html')

    recipients = get_recipients(recipients_file)
    subject, body = get_email_content(subject_file, body_file)
    attachment_paths = get_attachment_paths(attachments_folder)

    # Call send_emails_smtp to send emails
    send_emails_smtp(account, recipients, subject, body, attachment_paths, format_html)