
from xml.dom.minidom import parseString
#from xml.etree import ElementTree

def removeSYMBOL(text):
  return text.split(None, 1)[1].strip()

def prettyPrintXMLTxt(txt):
  return parseString(txt).toprettyxml(indent=' '*2)

#import xml.dom.minidom as md
#import sys

#def prettyPrintXMLTxt(txt):
# x.toprettyxml(indent=' '*2).split('\n') if line.strip()])
