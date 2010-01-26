class Node:
  '''A simple tree implementation'''
  def __init__(self,type,children=None,leaf=None):
    self.type = type
    if children:
      self.children = children
    else:
      self.children = [ ]
    self.leaf = leaf

  def __str__(self):
     ch = ""
     for c in self.children:
       if (ch != ""):
         ch += ","
       ch += str(c)
     r = "Node: " + self.type + ",(" + ch + ")"
     if (self.leaf):
       r += "," + str(self.leaf)
     return r

class NodeXmlConvertor:
  '''A visitor that converts a tree to its XML reprensentation, usefull for debugging the conversion from formulat to Tree'''
  def visit(self, node):
    'convert the node to an XML representation'
    if (node == None):
      raise MyException("Node is None !!!")
    result = self.nodeToXml(node)
    return result

  def nodeToXml(self, node):
    'recursive XML representation of the node'
    if (isinstance(node, str)):
      return node
    if (isNumber(node)):
      return "<" + instanceClassName(node) + ">" + str(node) + "</" + instanceClassName(node) + ">"

    ch = ""
    for c in node.children:
      if (isinstance(c, Node)):
#        print "____ instance " + str(type(c))
        if len(ch) > 0:
          ch += ","
        ch += self.nodeToXml(c)
      else:
#        print "____ type " + str(type(c))
        if len(ch) > 0:
          ch += ","
        ch += str(c)
    leafstr = ""
    if node.leaf:
      leafstr = "<leaf>" + self.nodeToXml(node.leaf) + "</leaf>"
    result = "<node><type>" + str(node.type) +  "</type><children>" + ch + "</children>" + leafstr + "</node>"
#    print result
    return result


def instanceClassName(x):
  '''Returns a String representation of a instance's class name'''
  return type(x).__module__ + "." + type(x).__name__

