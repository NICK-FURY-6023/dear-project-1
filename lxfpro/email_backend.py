"""
Custom Email Backend - Sends emails AND prints to console
Perfect for development/demo - best of both worlds!
"""
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend


class DualEmailBackend(SMTPBackend):
    """
    Custom email backend that:
    1. Sends actual emails via SMTP (Gmail)
    2. Also prints to console/terminal
    
    Perfect for demo - users get email AND you can see in terminal!
    """
    
    def send_messages(self, email_messages):
        """Send emails via SMTP and print to console"""
        
        # 1. Print to console first (for immediate visibility)
        console_backend = ConsoleBackend()
        console_backend.send_messages(email_messages)
        
        # 2. Send actual emails via SMTP (parent class)
        try:
            smtp_result = super().send_messages(email_messages)
            return smtp_result
        except Exception as e:
            print(f"⚠️ SMTP send failed: {e}")
            # Return 0 to indicate failure, but email was still printed to console
            return 0
