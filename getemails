import imaplib
import email
from datetime import datetime, timedelta
import os

def fetch_recent_emails():
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_APP_PASSWORD"))
        mail.select("inbox")

        # Calculate date 24 hours ago
        since_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

        # Search for emails since yesterday
        status, messages = mail.search(None, f'(SINCE "{since_date}")')
        email_ids = messages[0].split()

        for e_id in email_ids:
            try:
                _, msg_data = mail.fetch(e_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Print bold & underlined subject
                print("\n\033[1;4m" + msg['subject'] + "\033[0m")  # Bold underline
                
                # Get and print body text
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors='replace')
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors='replace')
                
                print("\n" + body.strip() + "\n")
                print("-" * 50)  # Separator line

            except Exception as e:
                print(f"\nError processing email: {str(e)}")
                continue

    except Exception as e:
        print(f"IMAP connection error: {str(e)}")
    finally:
        if 'mail' in locals():
            try:
                mail.close()
            except:
                pass
            try:
                mail.logout()
            except:
                pass

if __name__ == "__main__":
    fetch_recent_emails()  # Fixed typo in function name
