#coding: utf-8

import sys, commands, time, socket, datetime
sys.path.append("/home/newmoni/workspace")

import utils.src.mqutils as mqutils

def send(avg):
    target_user = open("./target_user", "r")
    target_user = target_user.readlines()[0]

    mqutils.send_mq("35.buzzni.com", "noti", {"title":"WARN : %s is too hot" % str(socket.gethostname()),
                                              "content":"loadavg : %s      // %s" % (str(avg), str(datetime.datetime.now())),
                                              "target":[target_user]})

def start():
    while 1:
        try:
            result = commands.getoutput("cat /proc/loadavg").split(" ")[0]
            avg = float(result)
            if avg >= 0.0:
                send(avg)
                print "send!"
                time.sleep(1)
            print "rotate"
            time.sleep(1)
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
