from src.bulk_mail import send_bulk_emails

if __name__ == "__main__":
    # Configuration
    email_account_name = "TRISTOKORUN"  # Name of the account as defined in .env
    recipients_filename = "recipients.txt"  # Recipients file in the data folder
    subject_filename = "subject.txt"  # Subject file in the data folder
    body_filename = "body.html"  # Email body file (body.txt for plain text or body.html for HTML)

    # Send bulk emails
    send_bulk_emails(
        account_name=email_account_name,
        recipients_filename=recipients_filename,
        subject_filename=subject_filename,
        body_filename=body_filename
    )