from vgsn_autogen import *
import os
from fileset import *

if __name__ == '__main__':
  link = "/home/jerome/Code/Customers/JB/Maths/WEB/pdfs"
  if not os.path.exists(link):
    print "WARNING: link " + link + " doesn't exist"
    link = None
  m = Monitor(FileSet("testdata/interfaces", "**.xls").find_paths(), 'data/oppgaver4.txt', link)
  m.run()
