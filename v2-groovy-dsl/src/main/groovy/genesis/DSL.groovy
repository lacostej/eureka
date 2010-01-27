class DSL {
  static def random = new Random()

  static random(list) {
    return list[random.nextInt(list.size())]
  }

  static add(a,b) {
    return a + b 
  }

  static sub(a,b) {
    return a - b 
  }

  static sign1(a, b) {
    return random([DSL.&add, DSL.&sub])(a,b)
  }

  static signe1() {
    return random([DSL.&add, DSL.&sub])
  }

  static int r(range) {
    return random(range)
  }

  static solve(expression) {
    return "" + expression
  }
}

/** a simple tree implementation **/
class ENode {
  def type
  def children = []

  ENode(type, children) {
    this.type = type
    this.children = children
  }

  String toString() {
    return "Node " + type  + ",("+ children.join(',') + ")"
  }
}

class MyException extends RuntimeException {
  MyException(s) { super(s) } 
}


/* A visitor that converts a tree to its XML reprensentation, usefull for debugging the conversion from formulat to Tree */
class NodeXmlConvertor {
  /* convert the node to an XML representation */
  def visit(self, node) {
    if (node == None)
      throw new MyException("Node is None !!!")
    result = this.nodeToXml(node)
    return result
  }

  /* recursive XML representation of the node */
  def nodeToXml(node) {
    return null;
  }
}
/*
    if (isinstance(node, str)) {
      return node
    }
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

class NodeResultEvaluator:
  '''A visitor that go through the tree and computes the values of the sub-tree wrapped inside a 'result' node'''
  rec_count = 0

  def visit(self, node):
    'conver result expressions into their values whenever possible'
#    print "EVALUATING " + toXmlConvertor.visit(node)
    r = self.evaluateResult(node)
#    print "EVALUATED " + toXmlConvertor.visit(r)
    return r

  def evaluateResult(self, node, evaluate=False):
    self.rec_count += 1
    if (not isinstance(node, Node)):
      self.rec_count -= 1
      return node

    if (node.type == "result"):
      r = self.evaluateResult(node.children[0], True)
      self.rec_count -= 1
      return r

    n = self.evaluate(node, evaluate)
    if (n != None):
      self.rec_count -= 1
      return n

    newtype = node.type
    children = []
    newleaf = None

    for child in node.children:
      children.append(self.evaluateResult(child, evaluate))
    if (node.leaf):
      newleaf = self.evaluateResult(node.leaf, evaluate)
    node = Node(newtype, children, newleaf)
    n2 = self.evaluate(node, evaluate)
    if (n2 != None):
      node = n2
    self.rec_count -= 1
    return node

#  def power(self, i, j):

  def evaluate(self, node, evaluate):
#    print (' '*self.rec_count) + "EVALUATING " + str(evaluate) + " " + toXmlConvertor.visit(node)
    r = self.theevaluate(node, evaluate)
#    if (r):
#      print (' '*self.rec_count) + "EVALUATED " + str(evaluate) + " " + toXmlConvertor.visit(r)
    return r

  def theevaluate(self, node, evaluate):
#    print "EVALUATING " + str(evaluate) + " " + toXmlConvertor.visit(node) + " " + node.type + " " + str(type(node.children[0])) + " "
#    print type(node.children)
#    print type(node.children[0])

    # vars are always evaluated
    if isNumber(node):
      return node
    if ((node.type == 'int' or node.type == 'decimal') and isNumber(node.children[0])):
#      print "EVALUATING var " + str(node.children)
      return node.children[0]
    if (node.type == 'var' and isNumber(node.children[0])):
#      print "EVALUATING var " + str(node.children)
      return node.children[0]

    if (node.type == 'stdform' and isNumber(node.children[0])):
      return node

    if (node.type == 'decform' and isNumber(node.children[0])):
      return node

    if (node.type == 'list'):
      l = [self.evaluateResult(elem, evaluate) for elem in node.children]
      return Node("list", l)

    if (evaluate):
      if (node.type == 'equals'):
        return Node("equals", [self.evaluate(top, evaluate), self.evaluate(bottom, evaluate)])
      if (node.type == 'frac' and isInt(node.children[0]) and isInt(node.children[1])):
        return reduceToFracOrIntNode(node.children[0], node.children[1])
      if (node.type == "neg" and isNumber(node.children[0])):
        return -1 * node.children[0]
      if (node.type == 'frac' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return decimal.Decimal(node.children[0]) / decimal.Decimal(node.children[1])
      if (node.type == 'paren' and isNumber(node.children[0])):
        return node.children[0]
      if (node.type in ['*', ':'] and isparen(node.children[0])):
        return self.evaluate(Node(node.type, [node.children[0].children[0], node.children[1]]), evaluate)
      if (node.type in ['*', ':'] and isparen(node.children[1])):
        return self.evaluate(Node(node.type, [node.children[0], node.children[1].children[0]]), evaluate)
      if (node.type == '^' and isInt(node.children[1])):
        if (node.children[1] == 0):
          return 1
        if (node.children[1] == 1):
          return self.evaluate(node.children[0], evaluate)
      if (node.type == '^' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return decimal.getcontext().power(decimal.Decimal(node.children[0]), decimal.Decimal(node.children[1]))
      if (node.type == '-' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return node.children[0] - node.children[1]
      if (node.type == '+' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return node.children[0] + node.children[1]
      if (node.type == '*' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return node.children[0] * node.children[1]
      if (node.type == ':' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return decimal.Decimal(node.children[0]) / node.children[1]
      if ((node.type == '+' or node.type == '-') and isIntOrFracInt(node.children[0]) and isIntOrFracInt(node.children[1])):
        sign = 1
        if (node.type=='-'):
          sign = -1
        top = topIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1]) + sign * topIntOrFracInt(node.children[1]) * bottomIntOrFracInt(node.children[0])
        bottom = bottomIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        return reduceToFracOrIntNode(top, bottom)
      if ((node.type == '*') and isIntOrFracInt(node.children[0]) and isIntOrFracInt(node.children[1])):
        top = topIntOrFracInt(node.children[0]) * topIntOrFracInt(node.children[1])
        bottom = bottomIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        return reduceToFracOrIntNode(top, bottom)
      if ((node.type == ':') and isIntOrFracInt(node.children[0]) and isIntOrFracInt(node.children[1])):
        top = topIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        bottom = bottomIntOrFracInt(node.children[0]) * topIntOrFracInt(node.children[1])
        return reduceToFracOrIntNode(top, bottom)
#      return node

def isparen(node):
  return isinstance(node, Node) and node.type == "paren"

def stdform(d):
  '''Returns the standard form representation of a number as a string'''
  if (isinstance(d, int)):
    d = decimal.Decimal(d)
  if (not isinstance(d, decimal.Decimal)):
    print "ERROR :" + str(type(d)) + " " + str(d)

    #print str(10**(-d.adjusted()))
  s = str((d*decimal.Decimal(str(10**(-d.adjusted())))).normalize().quantize(decimal.Decimal("0.00")).normalize())
  if (d.adjusted() != 0):
#    s += "E" + str(d.adjusted())
    s += " * 10^" + str(d.adjusted())
  return s

def decform(d):
  '''Returns the full representation of a number as a string'''
  if (isInt(d)):
    return str(d)
#  print "DECFORM " + str(type(d)) + " " + __decstr(d)
  return __decstr(d)

def __decstr(d):
  '''Return string representation of the decimal in scientific notation.
   Captures all of the information in the underlying representation.
   VARIATION FROM PYTHON2.6 decimal.Decimal.__str__ where scientitic notation doesn't exist
  '''

  sign = ['', '-'][d._sign]
  if d._is_special:
    if d._exp == 'F':
      return sign + 'Infinity'
    elif d._exp == 'n':
      return sign + 'NaN' + d._int
    else: # self._exp == 'N'
      return sign + 'sNaN' + d._int

  # number of digits of self._int to left of decimal point
  leftdigits = d._exp + len(d._int)

  # dotplace is number of digits of self._int to the left of the
  # decimal point in the mantissa of the output string (that is,
  # after adjusting the exponent)
  if d._exp <= 0 and leftdigits > -100:
    # no exponent required
    dotplace = leftdigits
  elif not eng:
    # usual scientific notation: 1 digit on left of the point
    dotplace = 1
  elif d._int == '0':
    # engineering notation, zero
    dotplace = (leftdigits + 1) % 3 - 1
  else:
    # engineering notation, nonzero
    dotplace = (leftdigits - 1) % 3 + 1

  if dotplace <= 0:
    intpart = '0'
    fracpart = '.' + '0'*(-dotplace) + d._int
  elif dotplace >= len(d._int):
    intpart = d._int+'0'*(dotplace-len(d._int))
    fracpart = ''
  else:
    intpart = d._int[:dotplace]
    fracpart = '.' + d._int[dotplace:]
  if leftdigits == dotplace:
    exp = ''
  else:
    if context is None:
      context = getcontext()
      exp = ['e', 'E'][context.capitals] + "%+d" % (leftdigits-dotplace)

  return sign + intpart + fracpart + exp

def stdformLatex(d):
  '''Returns the standard form representation of a number as a string'''
  if (isinstance(d, int)):
    d = decimal.Decimal(d)
  if (not isinstance(d, decimal.Decimal)):
    print "ERROR :" + str(type(d)) + " " + str(d)
    #print str(10**(-d.adjusted()))
  s = str((d*decimal.Decimal(str(10**(-d.adjusted())))).normalize().quantize(decimal.Decimal("0.00")).normalize())
  if (d.adjusted() != 0):
    s += " \cdot 10^{" + str(d.adjusted()) + "}"
  return s

def topIntOrFracInt(intOrFrac):
  '''Returns the top of a fraction of integers or the integer value. Used to compute fracOrInt operations'''
  if (not isIntOrFracInt(intOrFrac)):
    raise MyException(str(intOrFrac) + " of type " + str(type(intOrFrac)))
#  print toXmlConvertor.visit(intOrFrac)
  if isInt(intOrFrac):
    return intOrFrac
  return intOrFrac.children[0]

def bottomIntOrFracInt(intOrFrac):
  '''Returns the bottom of a fraction of integers or the integer value. Used to compute fracOrInt operations'''
  if (not isIntOrFracInt(intOrFrac)):
    raise MyException(str(intOrFrac) + " of type " + str(type(intOrFrac)))
#  print toXmlConvertor.visit(intOrFrac)
  if isInt(intOrFrac):
    return 1
  return intOrFrac.children[1]

def reduceToFracOrIntNode(top, bottom):
  top, bottom = reduceFrac(top, bottom)
  if (bottom != 1):
    negative = top < 0
    n = Node("frac", [abs(top), bottom])
    if (negative):
      n = Node("neg", [n])
    return n
  else:
    return top

def reduceFrac(top, bottom):
  '''Reduces a fraction of integers. E.g. 30,35 -> 6,7. Returns a new couple of integers representing the fraction. top can be positive.'''

  if (bottom == 0):
    return top, bottom

  sign = 1
  if (top * bottom < 0):
    sign = -1

  top = abs(top)
  bottom = abs(bottom)

  a = split(top)
  b = split(bottom)
  x = 0
  while x < len(a):
    i = a[x]
    if (i in b):
      a.remove(i)
      b.remove(i)
      top = top / i
      bottom = bottom / i
    else:
      x += 1
  return sign*top, bottom

def isIntOrFracInt(x):
  '''Returns True if the parameter is an int or fraction of integers.'''
  return isinstance(x, int) or (isinstance(x, Node) and x.type == "frac" and isinstance(x.children[0], int) and isinstance(x.children[1], int))

def isInt(x):
  '''Returns True if the parameter is an int.'''
  return isinstance(x, int)

def isDecimal(x):
  '''Returns True if the parameter is an decimal.'''
  return isinstance(x, decimal.Decimal)

def isNumber(x):
  '''Returns True if the parameter is an int or decimal.'''
  return isInt(x) or isDecimal(x)

def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()

def formatNumber(node):
  if (isinstance(node, int)):
    return str(node)
  TWOPLACES = decimal.Decimal('0.01')
  return str(remove_exponent(node.quantize(TWOPLACES)))

class NodeFormulaSimpleOuptutGenerator:
  '''A tree visitor that converts the formula to String. Simplified.'''

  binaryOperators = [ '+', '-', ':', '*']

  def visit(self, node):
    'conver result expressions into a String we can read'
    result = self.toString(node)
#    print "RESULT " + str(result)
    return result

  def toString(self, node):
#    print "toString: " + toXmlConvertor.visit(node)
    if (node == None):
      raise MyException("Node is None !")
    if (isNumber(node)):
      return formatNumber(node)
    if (isinstance(node, str)):
      return node
    if (node.type == 'list'):
      l = [self.toString(elem) for elem in node.children]
      return "(" + ",".join(l) + ")"
    if (node.type == "int"):
      return self.toString(node.children[0])
    if (node.type == "decimal"):
      return self.toString(node.children[0])
    if (node.type == "var"):
      result = self.toString(node.children[0])
      if (len(node.children) > 1):
        result += "=" + self.toString(node.children[1])
      return result
    if (node.type == "sqrt"):
      return "sqrt(" + self.toString(node.children[0]) + "," + self.toString(node.children[1]) + ")"
    if (node.type == "eller"):
      return self.toString(node.children[0]) + " eller " + str(self.toString(node.children[1]))
    if (node.type == "stdform"):
      if (isNumber(node.children[0])):
        return stdform(node.children[0])
      raise MyException("The following node cannot be converted through stdform. Evaluation error ? Node: " + self.toString(node.children[0]))
    if (node.type == "decform"):
      if (isNumber(node.children[0])):
        return decform(node.children[0])
      raise MyException("The following node cannot be converted through decform. Evaluation error ? Node: " + self.toString(node.children[0]))
    if (node.type == "neg"):
      return "-" + self.toString(node.children[0])
    if (node.type == "equals"):
      return self.toString(node.children[0]) + " = " + self.toString(node.children[1])
    if (node.type in self.binaryOperators):
      return str(self.toString(node.children[0])) + " " + node.type + " " + str(self.toString(node.children[1]))
    if (node.type == "paren"):
      return "(" + self.toString(node.children[0]) + ")"
    if (node.type == "frac"):
      return self.toString(node.children[0]) + "/" + self.toString(node.children[1])
    if (node.type == "^"):
      return self.toString(node.children[0]) + "^" + self.toString(node.children[1])

    if (node.type == "text"):
      return node.children[0]

#    if (node.type == "paren"):
#      return "(" + self.toString(node.children[0]) + ")"
    if (not isinstance(node, str)):
      raise MyException("Node isn't yet converted to String: " + str(node))
    return node

class NodeLatexConvertor():
  '''A tree visitor that converts the formula to its LaTex representation.'''

  binaryOperators = [ '+', '-', ':', '*']
  latexBinaryOperators = {
    '+': " + ",
    '-': " - ",
    ':': " \\div ",
    '*': " \\cdot ",
  }

  def visit(self, node):
    'conver result expressions into a String that LaTeX can understand'
    result = self.toString(node)
#    print "RESULT " + str(result)
    return result

  def toString(self, node):
    if (node == None):
      raise MyException("Node is None !")

#    print "DEBUG: toString: " + toXmlConvertor.visit(node)

    if (isNumber(node)):
      return formatNumber(node)
    if (isinstance(node, str)):
      return node
    if (node.type == 'list'):
      l = [self.toString(elem) for elem in node.children]
      return "(" + ",".join(l) + ")"
    if (node.type == "int"):
      return self.toString(node.children[0])
    if (node.type == "decimal"):
      return self.toString(node.children[0])
    if (node.type == "var"):
      result = self.toString(node.children[0])
      if (len(node.children) > 1):
        result += "=" + self.toString(node.children[1])
      return result
    if (node.type == "sqrt"):
      return "\\sqrt[" + self.toString(node.children[0]) + "]{" + self.toString(node.children[1]) + "}"
    if (node.type == "eller"):
      return self.visit(node.children[0]) + " eller " + self.visit(node.children[1])
    if (node.type == "stdform"):
      return stdformLatex(node.children[0])
    if (node.type == "decform"):
      return self.toString(decform(node.children[0]))
    if (node.type == "neg"):
      return "-" + self.toString(node.children[0])
    if (node.type == "equals"):
      return self.visit(node.children[0]) + " = " + self.visit(node.children[1])
    if (node.type in self.binaryOperators):
#      print "HI HI"
      return self.toString(node.children[0]) + self.latexBinaryOperators[node.type] + self.toString(node.children[1])
    if (node.type == "paren"):
      return "\\left(" + self.toString(node.children[0]) + "\\right)"
    if (node.type == "frac"):
      return "\\frac{" + self.toString(node.children[0]) + "}{" + self.toString(node.children[1]) + "}"
    if (node.type == "^"):
      return self.toString(node.children[0]) + "^{" + self.toString(node.children[1]) + "}"

    if (node.type == "text"):
#      print "text: " + node.children
      return node.children[0]

#    if (node.type == "paren"):
#      return "(" + self.toString(node.children[0]) + ")"
    if (not isinstance(node, str)):
      raise MyException("Node isn't yet converted to String: " + str(node))
    return node
*/
