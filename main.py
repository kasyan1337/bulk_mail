import os
from src.bulk_mail import send_bulk_emails, get_recipients

if __name__ == "__main__":
    # Configuration
    email_sender = "TUAN"  # Name of the account as defined in .env
    email_receiver = "recipients.txt"  # Recipients file in the email folder
    subject = "Random title"  # Enter the email subject directly here
    body = "body.html"  # Email body file (body.txt for plain text or body.html for HTML)
    content_folder = "email"

    # Define paths
    email_folder = os.path.join(os.path.dirname(__file__), content_folder)
    recipients_file = os.path.join(email_folder, email_receiver)
    content_path = os.path.join(email_folder, "intro.docx")  # Specify the content file path

    # Load recipients and display for confirmation
    recipients = get_recipients(recipients_file)
    print("\nRecipients:")
    print("\n".join(recipients))

    # Ask for confirmation before proceeding
    confirm = input("\nIs this the correct list of recipients? Type 'Y' to confirm: ").strip()
    if confirm.lower() == 'y':
        # Send bulk emails
        send_bulk_emails(
            account_name=email_sender,
            recipients_filename=email_receiver,
            subject=subject,
            body_filename=body,      # Pass body.html directly
            content_path=content_path if "CWT.html" in body or "WTM.html" in body else None  # Only pass content_path if using a template
        )
    else:
        print("Email sending cancelled.")