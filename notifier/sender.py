__author__ = "roman.subik"

import os
import smtplib

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

    def send_email(self, recipients, subject, query_results):
        sender = self.user
        to = recipients if type(recipients) is list else [recipients]
        message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % \
                  (sender, ", ".join(to), subject, EmailSender.create_body(query_results))

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

    @staticmethod
    def create_body(self, query_results):
        full_rapport = ''

        for query_title in query_results:
            result = query_results[query_title]

            if not result['total']:
                continue

            hits = result.get('hits', [])

            full_rapport += '<h3>{}</h3><br/>'.format('query_title')

            for hit in hits:
                item = hit['_score']
                full_rapport += flat_info_body.format(url=item.get('url', '?'),
                                                      title=item.get('title', '?'),
                                                      price=item.get('price', '?'),
                                                      size=item.get('size', '?'),
                                                      floor=item.get('floor', '?'),
                                                      score=hit.get('score')
                                                      )

        return email_body_template.format(full_rapport=full_rapport)
