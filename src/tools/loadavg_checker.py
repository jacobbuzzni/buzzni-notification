#coding: utf-8

import sys, commands, time, socket, datetime
sys.path.append("/home/newmoni/workspace")

import utils.src.mqutils as mqutils

def send(avg):
    mail_list = open("./mail_list", "r")
    mail_list = mail_list.read().replace("\n", "")
    mail_list = mail_list.split(",")

    mqutils.send_mq("35.buzzni.com", "noti", {"title":"WARN : %s is too hot" % str(socket.gethostname()),
                                              "content":"loadavg : %s      // %s" % (str(avg), str(datetime.datetime.now())),
                                              "target":mail_list})

def start():
    while 1:
        try:
            result = commands.getoutput("cat /proc/loadavg").split(" ")[0]
            avg = float(result)
            if avg >= 4.0:
                send(avg)
                time.sleep(25)
            time.sleep(5)
        except KeyboardInterrupt:
            exit(0)
        except IOError, e:
            print e
            exit(0)
        except Exception, e:
            print Exception
            print e


if __name__ == "__main__":
    start()
