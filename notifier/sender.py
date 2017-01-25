# -*- coding: utf-8 -*-
__author__ = "roman.subik"

import os
import smtplib
from email.message import Message

email_body_template = """
Dear recipients,<br/>
<br/>
I've found some cool flats, that you might want to check out:<br/>
<br/>
{full_rapport}<br/>
<br/>
Follow the links, to see more info!<br/>
<br/>
Best regards,<br/>
Your handy house-finder :)
"""

flat_info_body = """
Url: {url}<br/>
Title: {title}<br/>
Price: {price}<br/>
Size: {size}<br/>
Floor: {floor}<br/>
Match score: {score}<br/>
<br/>
"""


class EmailSender(object):
    def __init__(self):
        self.user = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASS')
        self.smtp_server = os.getenv('SMTP_SERVER')

    def send_email(self, recipients, subject, query_results):
        message = self._create_message(recipients, subject, query_results)

        try:
            self._send_message(recipients, message)
            print 'successfully sent the mail'
        except Exception as e:
            print "failed to send mail: {}".format(e)

    def _create_message(self, recipients, subject, query_results):
        message = Message()
        message['From'] = self.user
        message['To'] = ", ".join(recipients)
        message['Subject'] = subject.encode('utf-8')
        message.add_header('Content-Type', 'text/html')
        message.set_payload(self.create_body(query_results))

        return message

    def _send_message(self, recipients, message):
        server = smtplib.SMTP(self.smtp_server, 587)
        server.ehlo()
        server.starttls()
        server.login(self.user, self.password)
        server.sendmail(self.user, recipients, message.as_string())
        server.close()

    @staticmethod
    def create_body(query_results):
        full_rapport = ''

        for query_title in query_results:
            result = query_results[query_title]

            if not result['total']:
                continue

            hits = result.get('hits', [])

            full_rapport += '<h3>{}</h3><br/>'.format(query_title.encode('utf-8'))

            for hit in hits:
                item = hit['_source']
                full_rapport += flat_info_body.format(url=item.get('url', '?'),
                                                      title=item.get('title', '?').encode('utf-8'),
                                                      price=item.get('price', '?'),
                                                      size=item.get('size', '?'),
                                                      floor=item.get('floor', '?'),
                                                      score=hit.get('score')
                                                      )

        return email_body_template.format(full_rapport=full_rapport)
