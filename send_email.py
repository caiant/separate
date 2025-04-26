import yagmail
# Email credentials (use environment variables in production)
EMAIL_ADDRESS = "cailin.antonio@glccap.com"
EMAIL_PASSWORD = "ohdu zsxf lahi mpss"
TO_EMAILS = "lovelycailin@gmail.com
BCC_EMAILS = "caiantonio2427@gmail.com"



def send_email():
    """Send formatted market report via email"""
    try:
        # Get market data including BOE rate
        market_data = get_market_data()
        
        # Format report - you'll need to define decision_date or pass None
        report_html = format_html_report(market_data)  # or get this from somewhere
        subject = f"Daily Market Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Initialize yagmail
        yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
        yag.send(
            to=TO_EMAILS,
            subject=subject,
            contents=report_html, 
            bcc=BCC_EMAILS
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")

if __name__ == "__main__":
    send_email()
