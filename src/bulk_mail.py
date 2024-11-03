import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

from dotenv import load_dotenv


# Load email account details from environment variables
def load_accounts():
    accounts = {}
    load_dotenv()
    account_names = eval(os.getenv("EMAIL_ACCOUNTS"))
    for name in account_names:
        email = os.getenv(f"{name.upper()}_EMAIL")
        password = os.getenv(f"{name.upper()}_APP_PASSWORD") or os.getenv(
            f"{name.upper()}_PASSWORD"
        )
        smtp_server = os.getenv(f"{name.upper()}_SMTP_SERVER")
        smtp_port = os.getenv(f"{name.upper()}_SMTP_PORT")
        smtp_ssl = os.getenv(f"{name.upper()}_SMTP_SSL", "True") == "True"
        accounts[name] = {
            "name": name,
            "email": email,
            "password": password,
            "smtp_server": smtp_server,
            "smtp_port": int(smtp_port) if smtp_port else None,
            "smtp_ssl": smtp_ssl,
        }
    return accounts


# Load recipients from a file
def get_recipients(file_path):
    with open(file_path, "r") as file:
        data = file.read()
        recipients = [
            email.strip()
            for email in data.replace("\n", ",").replace(";", ",").split(",")
            if email.strip()
        ]
    return recipients


# Load email body content from a file
def get_email_body(body_path):
    # Define the path to the content.txt file
    content_path = os.path.join(os.path.dirname(body_path), "content.txt")

    # Check if the body_path is a specific template that requires content from content.txt
    if os.path.basename(body_path) in ["CWT.html", "WTM.html"]:
        with open(body_path, "r") as template_file:
            html_template = template_file.read()
        with open(content_path, "r") as txt_file:
            main_content = txt_file.read()

        # Convert plain text from content.txt to HTML format
        main_content_html = "<p>" + re.sub(r'\n\n+', '</p><p>', main_content).replace('\n', '<br>') + "</p>"

        # Replace the placeholder in the template with the content
        final_body = html_template.replace("{{ main_content }}", main_content_html)
    else:
        # For other files, just read the content as-is
        with open(body_path, "r") as file:
            final_body = file.read()

    return final_body


# Get file paths for any attachments
def get_attachment_paths(folder_path):
    if os.path.exists(folder_path):
        return [
            os.path.join(folder_path, filename)
            for filename in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, filename))
        ]
    return []


# New send_emails_smtp function using smtplib and MIMEText
# New send_emails_smtp function using smtplib and MIMEText
def send_emails_smtp(account, recipients, subject, body, attachment_paths, format_html):
    try:
        # Set up the SMTP server
        if "gmail" in account["email"].lower():
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_ssl = False
        else:
            smtp_server = account["smtp_server"]
            smtp_port = account["smtp_port"]
            smtp_ssl = account["smtp_ssl"]

        if smtp_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

        server.login(account["email"], account["password"])

        # Define custom display names for each account
        display_names = {
            "CWT": "Kasim Janci (CWT)",
            "WTM": "Kasim Janci (WTM)",
            "TRISTOKORUN": "流沙奶黄包粉丝"
            # Add other accounts and display names as needed
        }

        # Determine the display name, or default to the email address if no display name is found
        from_name = display_names.get(account["name"], account["email"])
        from_address = f"{from_name} <{account['email']}>"

        for recipient in recipients:
            # Set up the MIME message structure
            msg = MIMEMultipart("alternative")
            msg["From"] = from_address
            msg["To"] = recipient
            msg["Subject"] = subject

            # Attach the HTML or plain text content
            if format_html:
                html_part = MIMEText(body, "html")
                msg.attach(html_part)
            else:
                text_part = MIMEText(body, "plain")
                msg.attach(text_part)

            # Attach any files
            if attachment_paths:
                for attachment_path in attachment_paths:
                    with open(attachment_path, "rb") as f:
                        attachment = MIMEText(f.read(), "base64", "utf-8")
                        attachment.add_header(
                            "Content-Disposition",
                            "attachment",
                            filename=os.path.basename(attachment_path),
                        )
                        msg.attach(attachment)

            # Send the email
            server.sendmail(account["email"], recipient, msg.as_string())
            print(f"Email sent to {recipient}")

        # Close the server connection
        server.quit()

    except Exception as e:
        print(f"Failed to send email: {e}")


# Main function to initiate the bulk email sending process
def send_bulk_emails(account_name, recipients_filename, subject, body_filename):
    # Check if body_filename requires specific account_name
    if body_filename == "CWT.html" and account_name != "CWT":
        print("Error: When using CWT.html as body, the email_sender must be 'CWT'.")
        return
    elif body_filename == "WTM.html" and account_name != "WTM":
        print("Error: When using WTM.html as body, the email_sender must be 'WTM'.")
        return

    # Load accounts
    accounts = load_accounts()
    if account_name not in accounts:
        print(f"Account '{account_name}' not found.")
        return
    account = accounts[account_name]

    # Define file paths for data
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../email")
    attachments_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "attachments"
    )

    recipients_file = os.path.join(data_folder, recipients_filename)
    body_file = os.path.join(data_folder, body_filename)

    # Automatically determine format_html based on the body file extension
    format_html = body_filename.endswith(".html")

    recipients = get_recipients(recipients_file)
    body = get_email_body(body_file)
    attachment_paths = get_attachment_paths(attachments_folder)

    # Call send_emails_smtp to send emails
    send_emails_smtp(account, recipients, subject, body, attachment_paths, format_html)
