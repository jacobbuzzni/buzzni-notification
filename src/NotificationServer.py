#!/usr/bin/env python
#coding: utf-8

import sys
sys.path.append("/home/newmoni/workspace")

import pika, json, datetime
from utils.src.mail import Sender
from utils.src.optparserutils import make_optparser

class NotificationServer(object):
    def __init__(self, mail_account, mq_server, queue_name):
        self.mq = pika.BlockingConnection()

        def set_mail_account():
            string = open(mail_account, "r")
            string = string.read()
            id, pw = string.split(",")
            return Sender("gmail", id, pw)
        self.mail = set_mail_account()
        self.mq = pika.BlockingConnection(pika.ConnectionParameters(host=mq_server))
        self.q_name = queue_name

    def _send_mail(self, target=[], title="", content=""):
        return self.mail.send_mail(target, title, content)

    def mq_callback(self, ch, method, properties, body):
        try:
            req = json.loads(body)
            target = req["target"]
            title = req["title"]
            content = req["content"]
            self._send_mail(target, title, content)
            print "="*50
            print "SUCCESS : %s" % (str(datetime.datetime.now()))
            print "%s" % (body)
        except:
            print "FAIL.. %s" % (body)

    def listen(self):
        chan = self.mq.channel()
        chan.queue_declare(queue=self.q_name)

        chan.basic_consume(self.mq_callback, queue=self.q_name, no_ack=True)

        print "[+] start listen.."
        chan.start_consuming()

if __name__ == '__main__':
    usage_str = "%prog [options] \n Description: buzzni email notification server.( using rabbitMQ )"
    options = [
        {
            "name": "mail_account",
            "default": "./mail_account.secret",
            "description": "set gmail account.( split by ',' )"
        },
        {
            "name": "mq_server",
            "default": "localhost",
            "description": "set rabbitmq server"
        },
        {
            "name": "queue_name",
            "default": "noti",
            "description": "set rabbitmq's queue name"
        }
    ]
    options, args = make_optparser(usage_str, options)
    tmp = NotificationServer(options.mail_account, options.mq_server, options.queue_name)
    tmp.listen()
