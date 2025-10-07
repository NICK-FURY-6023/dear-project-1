"""
Custom Email Backend - Sends emails AND prints to console
Perfect for development/demo - best of both worlds!
"""
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend


class DualEmailBackend:
    """
    Custom email backend that:
    1. Sends actual emails via SMTP (Gmail)
    2. Also prints to console/terminal
    
    Perfect for demo - users get email AND you can see in terminal!
    """
    
    def __init__(self, *args, **kwargs):
        # Initialize both backends
        self.smtp_backend = SMTPBackend(*args, **kwargs)
        self.console_backend = ConsoleBackend(*args, **kwargs)
    
    def send_messages(self, email_messages):
        """Send emails via SMTP and print to console"""
        
        # 1. Print to console first (for immediate visibility)
        console_result = self.console_backend.send_messages(email_messages)
        
        # 2. Send actual emails via SMTP
        smtp_result = self.smtp_backend.send_messages(email_messages)
        
        # Return number of emails sent
        return smtp_result
    
    def open(self):
        """Open both backends"""
        self.smtp_backend.open()
        self.console_backend.open()
    
    def close(self):
        """Close both backends"""
        self.smtp_backend.close()
        self.console_backend.close()
