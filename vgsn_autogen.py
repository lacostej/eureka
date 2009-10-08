import glob,os,stat,time
import traceback

import pdfsgen
from memutils import *


class Monitor:
  values = {}

  def __init__(self, interfaces, exoDatabaseFile, link=None):
    self.exoDatabaseFile = exoDatabaseFile
    self.interfaces = interfaces
    self.link = link

  def checkSum(self, files):
    '''Return a long which can be used to know if any files have changed.'''
    val = 0
    for f in files:
      stats = os.stat (f)
      val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
    return val

  def run(self):
    for f in self.interfaces:
      self.values[f] = self.checkSum([f, self.exoDatabaseFile])

    pwd = os.path.abspath(".")
    while (True):
      for f in self.interfaces:
#        print pwd
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

      time.sleep(1)

if __name__ == '__main__':
  link = "/home/vgsn/webapps/static_files/matte/pdfs"
  if not os.path.exist(link):
    print "WARNING: link " + link + " doesn't exist"
    link = None
  m = Monitor(FileSet("matte/interfaces", "**.xls").find_paths(), 'matte/oppgaver4.txt', link)
  m.run()
