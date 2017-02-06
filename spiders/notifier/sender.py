# -*- coding: utf-8 -*-
__author__ = "roman.subik"

import os
import smtplib
from email.message import Message

email_body_template = """
<h3>Dear recipients!<br/>
<br/>
I've found some cool flats, that you might want to check out:<br/>
</h3>
<br/>
<table cellpadding="5">
    <tr bgcolor="#e6f7ff">
        <th><big>Title</big></th>
        <th><big>Price</big></th>
        <th><big>Size</big></th>
        <th><big>Location</big></th>
        <th><big>Floor</big></th>
        <th><big>Score</big></th>
    </tr>
    {full_rapport}
</table>
<br/>
<br/>
<h3>
Follow the links, to see more info!<br/>
<br/>
Best regards,<br/>
Your handy house-finder :)
</h3>
"""

flat_info_body = """
    <tr bgcolor="{color}">
        <td><img src="{image}" width="133" height="100"/><br/><a href="{url}">{title}</a></td>
        <td align="right">{price}</td>
        <td align="right">{size}</td>
        <td align="right">{query}</td>
        <td align="right">{floor}</td>
        <td align="right">{score}</td>
    <tr/>
"""


class EmailSender(object):
    def __init__(self):
        self.user = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASS')
        self.smtp_server = os.getenv('SMTP_SERVER')

    def send_email(self, recipients, subject, query_results):
        message = self._create_message(recipients, subject, query_results)

        if not message:
            print 'Nothing to notify about today'
            return

        try:
            self._send_message(recipients, message)
            print 'Successfully sent the mail'
        except Exception as e:
            print "Failed to send mail: {}".format(e)
            raise e

    def _create_message(self, recipients, subject, query_results):
        body = self.create_body(query_results)

        if not body:
            return None

        message = Message()
        message['From'] = self.user
        message['To'] = ", ".join(recipients)
        message['Subject'] = subject.encode('utf-8')
        message.add_header('Content-Type', 'text/html')
        message.set_payload(body)

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
        total_hits = 0

        for query_title in query_results:
            result = query_results[query_title]

            if not result['total']:
                continue

            hits = result.get('hits', [])
            counter = 0

            for hit in hits:
                item = hit['_source']
                first_image = reduce(lambda x,y: x or y, item.get('images', []))
                full_rapport += flat_info_body.format(url=item.get('url', '?'),
                                                      image=first_image,
                                                      title=item.get('title', '?').encode('utf-8'),
                                                      price=str(item.get('price', '?')) + ' PLN'.encode('utf-8'),
                                                      size=str(item.get('size', '?')) + " m^2",
                                                      query=query_title.encode('utf-8'),
                                                      floor=item.get('floor', '?'),
                                                      score=round(float(hit.get('_score')), 2),
                                                      color='#e6f7ff' if counter % 2 else '#f0f5f5'
                                                      )

                counter += 1

            total_hits += counter

        if not total_hits:
            return None

        return email_body_template.format(full_rapport=full_rapport)
