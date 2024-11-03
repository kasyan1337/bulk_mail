from src.bulk_mail import send_bulk_emails

if __name__ == "__main__":
    # Configuration
    email_sender = "TRISTOKORUN"  # Name of the account as defined in .env
    email_receiver = "recipients.txt"  # Recipients file in the data folder
    subject = "Your Email Subject Here"  # Enter the email subject directly here
    body = "body.html"  # Email body file (body.txt for plain text or body.html for HTML)

    # Send bulk emails
    send_bulk_emails(
        account_name=email_sender,
        recipients_filename=email_receiver,
        subject=subject,
        body_filename=body
    )
