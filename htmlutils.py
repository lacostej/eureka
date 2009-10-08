import os

def gen_index(directory, indexFileName="index.html"):
  '''Generate an index file'''
  indexFile = os.path.join(directory, indexFileName)
  with open(indexFile, "w") as f:
    f.write(header())
    f.write(dirs(directory))
    f.write(files(directory))
    f.write(footer())

def header(title = "Directory Listing"):
  return '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>%s</title>
</head>
<h1>%s</h1>
<a href="..">[parent directory]</a><br/>
''' % (title, title)

def dirs(directory):
  l = sortedListDir(directory, os.path.isdir)
  text = []
  for x in l:
    text.append('<a href="%s">%s/ </a><br/>\n' % (x, x))
  return "".join(text)

def files(directory):
  l = sortedListDir(directory, os.path.isfile)
  text = []
  for x in l:
    text.append('<a href="%s">%s </a><br/>\n' % (x, x))
  return "".join(text)

def footer():
  return "</body></html>\n"

def filterOp_wrapper(filterOp, directory):
  def func(f):
    return filterOp(os.path.join(directory, f))
  return func

def sortedListDir(directory, filterOp):
  files = filter(filterOp_wrapper(filterOp, directory), os.listdir(directory))
  files.sort()
  return files

def x():
  l = [ os.path.join(directory, f) for f in  os.listdir(directory) ]
  files = filter(filterOp, l)
  files.sort()
  return [ os.path.basename(f) for f in files ]

if __name__ == "__main__":
  gen_index(".")


