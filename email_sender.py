"""
It is a python script that enable the user to send emails to a single
or multiple users using Gmail account in python.

It uses Google App password to gain access to Gmail account.
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender():
    """ Email sender using Gmail account in python.
    
    Attributes:
        gmail_address: 
            Gmail account used as sender address when sending emails
        app_password: 
            Google App password used to gain access to the gmail address given
    """
    def __init__(self):
        self.port = 587
        self.smtp_server = 'smtp.gmail.com'
        self.gmail_address, self.app_password = self.user_credentials()

    def user_credentials(self):
        """ If saved user credential is found, read that credential 
            and return Gmail address and Google App password, which
            is used to gain access to the Gmail account.

            Otherwise get user credentials and save to a file for
            later use so that it will not ask the user to provide
            credentials every time the program runs.

        returns:
            gmail_address: used as sender address when sending emails
            app_password: used to gain access to the gmail address given
        """
        import os
        home_dir = os.path.expanduser('~/')
        full_path = os.path.join(home_dir, '.app-credentials.txt')

        if os.path.exists(full_path):
            with open(full_path, 'r') as file:
                gmail_address = file.readline().strip()
                app_password = file.readline().strip()
        else:
            gmail_address = self.get_valid_email()
            app_password = self.get_app_password()

            with open(full_path, 'w') as file:
                file.write(f'{gmail_address}\n')
                file.write(f'{app_password}\n')

        return (gmail_address, app_password)
    
    def get_valid_email(self):
        """ Get valid email address from user."""
        answer = input('\nEnter your Gmail address: \n').strip()
        # TODO: check for email validity using regular expressions
        return answer
    
    def get_app_password(self):
        """ Get the 16-digit Google App password to gain access to Gmail."""
        answer = input('\nEnter the 16-digit Google App password:\n').strip()
        if len(answer) == 16:
            return answer
        else:
            print('Please provide a valid Google App password.')
            self.get_app_password()

    def send(self, to_addr, subject, text, html='', attachments=[]):
        """ Send an email message to the receiver."""
        from_addr = self.gmail_address

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = from_addr
        message['To'] = to_addr

        plain_text = MIMEText(text, 'plain')
        html_text = MIMEText(html, 'html')

        message.attach(plain_text)
        message.attach(html_text)

        try:
            context = ssl.create_default_context()

            print('Connecting to Gmail...')
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls(context=context)
            server.login(self.gmail_address, self.app_password)

            print('Sending message...')
            server.sendmail(from_addr, to_addr, message.as_string())

            print('\nMessage has been sent.')
        except Exception as e:
            print(e)
            print(f'\n\n{"-"*70}\n'+
            f'If you keep getting this error message after retrying a few more times,\n'+
            f'first check your internet connection. If that\'s ok,\n'
            f'the Gmial address or App password you provide may be incorrect\n'
            f'So, go to your Home directory and delete ".app-credentials.txt" file\n'+
            f'(It is hidden by default) and run the program again.\n{"-"*70}')
        finally:
            server.quit()