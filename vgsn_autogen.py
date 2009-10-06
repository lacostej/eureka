import glob,os,stat,time
import traceback

import pdfsgen

def checkSum():
  '''Return a long which can be used to know if any .py files have changed.
  Only looks in the current directory.'''
  val = 0
  for f in ['matte/interface.xls', 'matte/oppgaver4.txt']:
    stats = os.stat (f)
    val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
  return val

def run():
  val=0
  newVal= 0
  pwd = os.path.abspath(".")
  while (True):
#    print pwd
    os.chdir(pwd)
    try:
      newVal = checkSum()
      if newVal != val:
        val = newVal
        print "val " + str(val)
        pdfsgen.main("matte/interface.xls", "matte/oppgaver4.txt")
    except Exception, e:
      print "ERROR: couldn't generate: " + str(e) 
      traceback.print_exc()

    time.sleep(1)

if __name__ == '__main__':
  run()
