import logging
import requests

class MailGun(object):
    base_url = "https://api.mailgun.net/v2"

    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def send_email(self, from_addr, to_addrs, subject, text=None, html=None):
        if not isinstance(to_addrs, list):
            to_addrs = [to_addrs]

        url = "%s/%s/messages" % (self.base_url, self.domain)
        resp = requests.post(url,
                             auth=("api", self.api_key),
                             data={
                                "from": from_addr,
                                "to": to_addrs,
                                "subject": subject,
                                "text": text,
                                "html": html,
                             })
        if not resp.ok:
            logging.error("Error sending email: %s", resp.json["message"])

        return resp.ok
