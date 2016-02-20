import json
import urllib2

url = 'https://api.postmarkapp.com/email/withTemplate'


class Mail(object):
    def __init__(self, server_root, from_addr, api_key):
        self.server_root = server_root
        self.from_addr = from_addr
        self.api_key = api_key

    def sign_up(self, username, email, key):
        values = {
            'From': self.from_addr,
            'To': email,
            'TemplateID': 426401,
            'TemplateModel': {
                'product_name': 'Voting System',
                'action_url': self.server_root + '/signup/' + key,
                'username': username,
                'sender_name': 'Yuto Matsuki'
            }
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Postmark-Server-Token': self.api_key
        }
        req = urllib2.Request(url, json.dumps(values), headers)
        resp = urllib2.urlopen(req)
        print(resp.read())
