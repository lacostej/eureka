# By Jeff Winkler, http://jeffwinkler.net

import glob,os,stat,time,os.path
import pynotify

'''
Watch for changes in all .py files. If changes, run nosetests. 
'''
def checkSum():
    ''' Return a long which can be used to know if any .py files have changed.
    Only looks in the current directory. '''
    val = 0
    for f in glob.glob ('*.txt') + glob.glob ('data/*.txt'):
        stats = os.stat (f)
        val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
    for f in glob.glob ('*.py'):
        stats = os.stat (f)
        val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
    for f in glob.glob ('tests/*.py'):
        stats = os.stat (f)
        val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
    for f in glob.glob ('*.kid'):
        stats = os.stat (f)
        val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]

    return val


def notifyFailure():
    if not pynotify.init("Markup"):
        return
    pwd = os.path.abspath(".")
    n = pynotify.Notification(os.path.basename(pwd) + " build failed.",
        pwd + ": nosetests failed")

    if not n.show():
        print "Failed to send notification"

def notifySuccess():
    if not pynotify.init("Markup"):
        return
    pwd = os.path.abspath(".")
    n = pynotify.Notification(os.path.basename(pwd) + " build successfull.",
        pwd + ": nosetests success")

    if not n.show():
        print "Failed to send notification"
  
val=0
oldRes = 0
firstBuild = True
while (True):
    keepOnNotifyingFailures = True
    if checkSum() != val:
        val=checkSum()
        res = os.system ('nosetests')
        print "res:" + str(res)
        if (res != 0):
          if (oldRes == 0 or keepOnNotifyingFailures):
            notifyFailure()
        else:
          if (oldRes != 0 or firstBuild):
            notifySuccess()
        firstBuild = False
    time.sleep(1)
    oldRes = res
