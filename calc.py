#!/usr/bin/env python

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
#
# Class-based example contributed to PLY by David McNab
# -----------------------------------------------------------------------------

import sys
#sys.path.insert(0,"../..")

#if sys.version_info[0] >= 3:
#    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os
import decimal

class MyException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class FormulaParser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        self.formulaLexer = lex.lex(module=self, debug=self.debug)
        self.parser = yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('calc > ')
            except EOFError:
                break
            if not s: continue
            self.parse(s)

    def parse(self, s):
      return self.parser.parse(s, lexer=self.formulaLexer)

class Node:
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
  return type(x).__module__ + "." + type(x).__name__

toXmlConvertor = NodeXmlConvertor()

class NodeResultEvaluator:
  def visit(self, node):
    'conver result expressions into their values whenever possible'
#    print "EVALUATING " + toXmlConvertor.visit(node)
    r = self.evaluateResult(node)
#    print "EVALUATED " + toXmlConvertor.visit(r)
    return r

  def evaluateResult(self, node, evaluate=False):
    if (not isinstance(node, Node)):
      return node

    if (node.type == "result"):
      return self.evaluateResult(node.children[0], True)

    # FIXME
    n = self.evaluate(node, evaluate)
    if (n != None):
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
    return node

#  def power(self, i, j):
    
  def evaluate(self, node, evaluate):
#
#    print "EVALUATING " + str(evaluate) + " " + toXmlConvertor.visit(node)
    r = self.theevaluate(node, evaluate)
#    if (r):
#      print "EVALUATED " + str(evaluate) + " " + toXmlConvertor.visit(r)
    return r
     
  def theevaluate(self, node, evaluate):
#    print "EVALUATING " + str(evaluate) + " " + toXmlConvertor.visit(node) + " " + node.type + " " + str(type(node.children[0])) + " "
#    print type(node.children)
#    print type(node.children[0])

    # vars are always evaluated
    if (node.type == 'int' and isNumber(node.children[0])):
#      print "EVALUATING var " + str(node.children)
      return node.children[0]
    if (node.type == 'var' and isNumber(node.children[0])):
#      print "EVALUATING var " + str(node.children)
      return node.children[0]

    if (node.type == 'stdform' and isNumber(node.children[0])):
      return stdform(node.children[0])

    if (evaluate):
      if (node.type == 'frac' and isInt(node.children[0]) and isInt(node.children[1])):
        return node
      if (node.type == 'frac' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return decimal.Decimal(node.children[0]) / decimal.Decimal(node.children[1])
      if (node.type == 'paren' and isNumber(node.children[0])):
        return node.children[0]
      if (node.type == '^' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return decimal.getcontext().power(decimal.Decimal(node.children[0]), decimal.Decimal(node.children[1]))
      if (node.type == '-' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return node.children[0] - node.children[1]
      if (node.type == '+' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return node.children[0] + node.children[1]
      if (node.type == '*' and isNumber(node.children[0]) and isNumber(node.children[1])):
        return node.children[0] * node.children[1]
      if (node.type == ':' and isNumber(node.children[0]) and isNumber(node.children[1])):
        # FIXME this can lead to problems if x / y with y > x and both ints
        return decimal.Decimal(node.children[0]) / node.children[1]
      if ((node.type == '+' or node.type == '-') and isIntOrFracInt(node.children[0]) and isIntOrFracInt(node.children[1])):
        sign = 1
        if (node.type=='-'):
          sign = -1
        top = topIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1]) + sign * topIntOrFracInt(node.children[1]) * bottomIntOrFracInt(node.children[0]) 
        bottom = bottomIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        top, bottom = reduceFrac(top, bottom)
        return Node("frac", [top, bottom])
      if ((node.type == '*') and isIntOrFracInt(node.children[0]) and isIntOrFracInt(node.children[1])):
        top = topIntOrFracInt(node.children[0]) * topIntOrFracInt(node.children[1]) 
        bottom = bottomIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        top, bottom = reduceFrac(top, bottom)
        return Node("frac", [top, bottom])
      if ((node.type == ':') and isIntOrFracInt(node.children[0]) and isIntOrFracInt(node.children[1])):
        top = topIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1]) 
        bottom = bottomIntOrFracInt(node.children[0]) * topIntOrFracInt(node.children[1])
        top, bottom = reduceFrac(top, bottom)
        return Node("frac", [top, bottom])

def stdform(d):
  if (isinstance(d, int)):
    d = decimal.Decimal(d)
  if (not isinstance(d, decimal.Decimal)):
    print "ERROR :" + str(type(d)) + " " + str(d)
   
    #print str(10**(-d.adjusted()))
  s = str((d*decimal.Decimal(str(10**(-d.adjusted())))).normalize().quantize(decimal.Decimal("0.00")).normalize())
  if (d.adjusted() != 0):
    s += "E" + str(d.adjusted())
  return s

def topIntOrFracInt(intOrFrac):
  if (not isIntOrFracInt(intOrFrac)):
    raise MyException(str(intOrFrac) + " of type " + str(type(intOrFrac)))
#  print toXmlConvertor.visit(intOrFrac)
  if isinstance(intOrFrac, int):
    return intOrFrac
  return intOrFrac.children[0]

def bottomIntOrFracInt(intOrFrac):
  if (not isIntOrFracInt(intOrFrac)):
    raise MyException(str(intOrFrac) + " of type " + str(type(intOrFrac)))
#  print toXmlConvertor.visit(intOrFrac)
  if isinstance(intOrFrac, int):
    return abs(intOrFrac)
  return intOrFrac.children[1]

def reduceFrac(top, bottom):

  if (bottom == 0):
    return top, bottom

  sign = 1
  if (top * bottom < 0):
    sign = -1

  top = abs(top)
  bottom = abs(bottom)

  a = split(top)
  b = split(bottom)
  for i in a:
    if (i in b):
      a.remove(i)
      b.remove(i)
      top = top / i
      bottom = bottom / i
  return sign*top, bottom

def split(a):
  '''return the list of prime divisors'''
  import math
  if (a == 1):
    return [1]
  else:
    array = []
    i = 2
    while (i < math.sqrt(a) + 1):
      if (a % i == 0):
        array.append(i)
        a = a / i
      else:
        i += 1
    return array

def isIntOrFracInt(x):
  return isinstance(x, int) or (isinstance(x, Node) and x.type == "frac" and isinstance(x.children[0], int) and isinstance(x.children[1], int))

def isInt(x):
  return isinstance(x, int)

def isDecimal(x):
  return isinstance(x, decimal.Decimal)

def isNumber(x):
  return isInt(x) or isDecimal(x)

class NodeFormulaSimpleOuptutGenerator:
  binaryOperators = [ '+', '-', ':', '*']

  def visit(self, node):
    'conver result expressions into a String we can read'
    result = self.toString(node)
#    print "RESULT " + str(result)
    return result

  def formatNumber(self, node):
    if (isinstance(node, int)):
      return str(node)
    return str(node.normalize())

  def toString(self, node):
#    print "toString: " + toXmlConvertor.visit(node)
    if (node == None):
      raise MyException("Node is None !")
    if (isNumber(node)):
      return self.formatNumber(node)
    if (isinstance(node, str)):
      return node
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
    if (node.type == "neg"):
      return "-" + self.toString(node.children[0])
    if (node.type == "equals"):
      return self.toString(node.children[0]) + " = " + self.toString(node.children[1])
    if (node.type in self.binaryOperators):
      return str(self.toString(node.children[0])) + " " + node.type + " " + str(self.toString(node.children[1]))
    if (node.type == "paren"):
      return "(" + self.toString(node.children[0]) + ")"
    if (node.type == "frac"):
#      return "(" + self.toString(node.children[0]) + "/" + self.toString(node.children[1]) + ")"
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
  binaryOperators = [ '+', '-', ':', '*']

  def visit(self, node):
    'conver result expressions into a String that LaTeX can understand'
    result = self.toString(node)
#    print "RESULT " + str(result)
    return result

  def formatNumber(self, node):
    if (isinstance(node, int)):
      return str(node)
    return str(node.normalize())

  def toString(self, node):
    if (node == None):
      raise MyException("Node is None !")

#    print "DEBUG: toString: " + toXmlConvertor.visit(node)

    if (isNumber(node)):
      return self.formatNumber(node)
    if (isinstance(node, str)):
      return node
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
      return "$$\\sqrt[" + self.toString(node.children[0]) + "]{" + self.toString(node.children[1]) + "}$$"
    if (node.type == "eller"):
      return self.toString(node.children[0]) + " eller " + str(self.toString(node.children[1]))
    if (node.type == "stdform"):
      return stdform(node.children[0])
    if (node.type == "neg"):
      return "-" + self.toString(node.children[0])
    if (node.type == "equals"):
      return self.toString(node.children[0]) + " = " + self.toString(node.children[1])
    if (node.type in self.binaryOperators):
      return str(self.toString(node.children[0])) + " " + node.type + " " + str(self.toString(node.children[1]))
    if (node.type == "paren"):
      return "(" + self.toString(node.children[0]) + ")"
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

class Calc(FormulaParser):

    tokens = (
        'NUMBER', 'DECIMAL',
        'PLUS','MINUS','POWER','TIMES','DIVIDE','EQUALS', #,'EXP'
        'LPAREN','RPAREN',
        'LBRACE','RBRACE',
        'VARNAME', 'SYMBOL','OR_SYMBOL','SQRTSYMBOL','RESULTSYMBOL','FRACSYMBOL','STDFORMSYMBOL',
        'TEXT'
        )

    # Tokens

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
#    t_EXP     = r'\*\*'
    t_TIMES   = r'\*'
    t_POWER   = r'\^'
    t_DIVIDE  = r':'
    t_EQUALS  = r'\='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
#    t_VARNAME = r'[a-zA-Z]'
#    t_RESULTSYMBOL = r'\\res'
#    t_FRACSYMBOL = r'\\frac'
#    t_SQRTSYMBOL = r'\\sqrt'
#    t_STDFORMSYMBOL = r'\\stdform'
#    t_OR_SYMBOL = r'eller'
    t_TEXT = r'".+"'

    symbols = { 
      '\\res' : "RESULTSYMBOL",
      '\\frac' : "FRACSYMBOL",
      '\\sqrt' : "SQRTSYMBOL",
      '\\stdform' : "STDFORMSYMBOL",
    }

    def t_SYMBOL(self, t):
        r'\\[a-z]+'
        t.type = self.symbols[t.value]
        return t

    def t_OR_SYMBOL(self, t):
        r'eller'
        return t

    def t_VARNAME(self, t):
        r'[a-zA-Z]'
        return t

    def t_DECIMAL(self, t):
        r'\d+\.\d+'
#        try:
        t.value = decimal.Decimal(t.value)
#        except ValueError:
#          
#            print("Decimal value too large %s" % t.value)
#            t.value = 0
        #print "parsed number %s" % repr(t.value)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        #print "parsed number %s" % repr(t.value)
        return t

#    def t_TEXT(sefl, t):
#        r'.+'
#        return t


    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('left', 'POWER'),
        ('right','UMINUS'),
        ('right', 'EQUALS'),
        )

    def find_var(self, x):
      try:      
        return self.names[x]
      except LookupError:
        sys.stderr.write("Undefined name '%s'\n" % x)
        raise

    # FIXME only top level expression can be text, right ?
    def p_expression_text(self, p):
       'expression : TEXT'
#       print "*** TEXT"
       p[0] = Node("text", [p[1]])

    def p_expression_multiple_expressions(self, p):
        'expression : VARNAME NUMBER EQUALS expression OR_SYMBOL VARNAME NUMBER EQUALS expression'
        p[0] = Node("eller", [Node("var", [p[1]+str(p[2]), p[4]]), Node("var", [p[6]+str(p[7]), p[9]])])

#    def p_expression_equals(self, p):
#        'expression : expression EQUALS expression'
#        p[0] = Node("equals", [p[1], p[3]])

    def p_expression_binop(self, p):
        """
        expression : expression EQUALS expression
                   | expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression POWER expression
                   | expression VARNAME expression
        """
        #print [repr(p[i]) for i in range(0,4)]
        ops = [ '+', '-', '*', ':', '^']
        if (p[2] == "="):
          p[2] = "equals"
        elif not p[2] in ops:
          p[2] = self.find_var(p[2])

        p[0] = Node(p[2], [p[1], p[3]])

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = Node("neg", [p[2]])

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = Node("paren", [p[2]])

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = Node("int", [p[1]])

    def p_expression_decimal(self, p):
        'expression : DECIMAL'
        p[0] = Node("decimal", [p[1]])

    def p_expression_var(self, p):
        'expression : VARNAME'
#        print "HANDLING " + p[1]
        v = self.find_var(p[1])
        p[0] = Node("var", [v])

    def p_expression_frac(self, p):
        'expression : FRACSYMBOL LBRACE expression RBRACE LBRACE expression RBRACE'
        p[0] = Node("frac", [p[3], p[6]])

    def p_expression_result(self, p):
        'expression : RESULTSYMBOL LBRACE expression RBRACE'
        p[0] = Node("result", [p[3]])

    def p_expression_sqrt(self, p):
        'expression : SQRTSYMBOL LBRACE expression RBRACE LBRACE expression RBRACE'
        p[0] = Node("sqrt", [p[3], p[6]])

    def p_expression_stdform(self, p):
        'expression : STDFORMSYMBOL LBRACE expression RBRACE'
        p[0] = Node("stdform", [p[3]])

    def p_error(self, p):
        if p:
            sys.stderr.write("Syntax error at '%s'\n" % p.value)
            raise MyException("Syntax error at '%s'" % p.value)
        else:
            sys.stderr.write("Syntax error at EOF\n")
            raise MyException("Syntax error at EOF")

if __name__ == '__main__':
    calc = Calc()
    calc.run()
