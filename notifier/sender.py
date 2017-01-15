__author__ = "roman.subik"

import os
import smtplib


class EmailSender(object):
    def __init__(self):
        self.user = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASS')

    def send_email(self, recipients, subject, body):
        sender = self.user
        to = recipients if type(recipients) is list else [recipients]
        message = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % (sender, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(sender, to, message)
            server.close()
            print 'successfully sent the mail'
        except Exception as e:
            print "failed to send mail: {}".format(e)