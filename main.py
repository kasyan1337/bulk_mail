from src.bulk_mail import send_bulk_emails

if __name__ == "__main__":
    # Configuration
    email_account_name = "WTM"  # Name of the account as defined in .env
    recipients_filename = "recipients.txt"  # Recipients file in the data folder
    subject_filename = "subject.txt"  # Subject file in the data folder
    body_filename = "body.html"  # Email body file (body.txt or body.html) in the data folder
    attachments = ["attachment.pdf"]  # List of attachment filenames in the data folder

    # Send bulk emails
    send_bulk_emails(
        email_account_name,
        recipients_filename,
        subject_filename,
        body_filename,
        attachments
    )