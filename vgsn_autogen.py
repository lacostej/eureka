import sys
import glob,os,stat,time
import traceback

import pdfsgen
from memutils import *
from fileset import *

class Monitor:
  values = {}

  def __init__(self, interfaces, exoDatabaseFile, restartFile, link=None):
    self.exoDatabaseFile = exoDatabaseFile
    self.interfaces = interfaces
    self.restartFile = restartFile
    self.link = link

  def checkSum(self, files):
    '''Return a long which can be used to know if any files have changed.'''
    val = 0
    for f in files:
      try:
        if os.access(f, os.FS_OK):
          stats = os.stat (f)
          val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
      except Exception:
        print "Failure..."
        continue
    return val

  def restartChecksum(self):
    return self.checkSum([self.restartFile])

  def run(self):
    restartVal = self.restartChecksum()
    for f in self.interfaces:
      self.values[f] = self.checkSum([f, self.exoDatabaseFile])

    pwd = os.path.abspath(".")
    while (True):
      for f in self.interfaces:
        print "checking " + str(f)
        sys.stdout.flush()
        os.chdir(pwd)
        val = self.values[f]
        try:
          newVal = self.checkSum([f, self.exoDatabaseFile])
          if newVal != val:
            val = newVal
            print "val " + str(val)
            self.values[f] = val
            pdfsgen.main(f, self.exoDatabaseFile, self.link)
            print_top_n(10)
        except Exception, e:
          print "ERROR: couldn't generate: " + str(e)
          traceback.print_exc()

      newRestartVal = self.restartChecksum()
      if newRestartVal != restartVal:
        print self.restartFile + " changed. Quiting..."
        return

      time.sleep(1)

if __name__ == '__main__':
  link = "/home/vgsn/webapps/static_files/matte/pdfs"
  if not os.path.exists(link):
    print "WARNING: link " + link + " doesn't exist"
    link = None
  # FIXME make it so we can dynamically add a new file without restarting
  m = Monitor(FileSet("matte/interfaces", "**.xls").find_paths(), 'matte/oppgaver4.txt', 'matte/restart', link)
  m.run()
