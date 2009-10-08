
from xml.dom.minidom import parseString
#from xml.etree import ElementTree

class MyException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def u(s):
  '''encode the specified unicode string to utf-8'''
  if s == None:
    return None
  return s.encode("utf-8")

def removeSYMBOL(text):
  return text.split(None, 1)[1].strip()

def prettyPrintXMLTxt(txt):
  return parseString(txt).toprettyxml(indent=' '*2)

#import xml.dom.minidom as md
#import sys

#def prettyPrintXMLTxt(txt):
# x.toprettyxml(indent=' '*2).split('\n') if line.strip()])


# http://tomayko.com/writings/cleanest-python-find-in-list-function

## Python 2.6
#def index(seq, f):
#    """Return the index of the first item in seq where f(item) == True."""
#    return next((i for i in xrange(len(seq)) if f(seq[i])), None)

# Python 2.5 or 2.4
def index(seq, f):
    """Return the index of the first item in seq where f(item) == True."""
    for index in (i for i in xrange(len(seq)) if f(seq[i])):
        return index

def find(seq, f):
    """Return the element of the first item in seq where f(item) == True."""
    for element in seq:
      if f(element):
        return element

def findall(seq, f):
    """Return all the element in seq where f(item) == True."""
    result = []
    for element in seq:
      if f(element):
        result.append(element)
    return result
