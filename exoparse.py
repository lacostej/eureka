#!/usr/bin/python

import sys
# Get the token map from the lexer.  This is required.
from exolex import *

# Build the lexer
import ply.lex as lex
import re

import calc
from utils import *

# various formula tree visitors
nodeXmlConvertor = calc.NodeXmlConvertor()
nodeResultEvaluator = calc.NodeResultEvaluator()
formulaTextOutput = calc.NodeFormulaSimpleOuptutGenerator()
nodeLatexConvertor = calc.NodeLatexConvertor()

def load():
  import calc

def unload():
  del sys.modules['calc']

class Executor:
  '''A simple Command pattern implementation'''
  def __init__(self, function, param):
    self.function = function
    self.param = param

  def execute(self):
    return self.function(self.param)

class Func:
  pass

def randomFrom(array):
  '''Return an element randomly from the specified array'''
  import random
  return array[random.randint(0, len(array) -1 )]

class List(Func):
  '''A function whose value is picked from the specified values list'''

  val = None

  def __init__(self, values):
    self.values = values

  def randomize(self):
    self.val = randomFrom(self.values)
#    print "randomized: List val: " + str(self.val) + " from " + str(self.values)
    return self.val

  def value(self):
    return self.val

  def __str__(self):
    return str(self.value())

class Constant(Func):
  '''A function whose value is picked is a constant'''
  val = None

  def __init__(self, value):
    self.val = value

  def randomize(self):
    return self.val

  def value(self):
    return self.val

  def __str__(self):
    return "Constant(" + str(self.value()) + ")"


class Range(Func):
  '''A function whose value is picked a specified range'''
  val = None

  def __init__(self, start, stop, exclude=None):
    self.start = start
    self.stop = stop
    self.exclude = exclude

  def randomize(self):
    theRange = range(self.start, self.stop + 1)
    if (self.exclude != None):
      theRange.remove(self.exclude)
    r = randomFrom(theRange)
    self.val = r
#    print "randomize: Range val: " + str(self.val)
    return self.val

  def value(self):
    return self.val

  def __str__(self):
    return "Range(" + str(self.value()) + " in " + str(self.start)+","+str(self.stop) + ")"

class DecimalRange(Func):
  '''A function whose value is picked a specified range of ints'''
  val = None

  def __init__(self, start, stop, exclude=None):
    self.start = start
    self.stop = stop
    self.exclude = exclude
    if (exclude != None):
      raise MyException("Exclude support not yet implemented for DecimalRange")

  def randomize(self):
    import random
    import decimal
    intr = 0
    while (intr == 0):
      intr = random.randint(self.start * 100, self.stop * 100)
    value=decimal.Decimal(intr)/100
    self.val = value
#    print "randomized: DecimalRange val: " + str(self.val)
    return self.val

  def value(self):
    return self.val

  def __str__(self):
    return "DecimalRange(" + str(self.value()) + " in " + str(self.start)+","+str(self.stop) + ")"

signOps=['+','-',':','*']
sign1Ops=['+', '-']
sign2Ops=['*', ':']
#sign3Ops=['', '-']

class PredefinedFunction(Func):
  def __init__(self, func_symbol):
    self.functions = { #Built in Function table
      '\sign' : Executor(randomFrom, signOps),
      '\sign1' : Executor(randomFrom, sign1Ops),
      '\sign2' : Executor(randomFrom, sign2Ops),
#      '\sign3' : Executor(randomFrom, sign3Ops)
    }
    self.function = self.functions[func_symbol]
    self.randomize()

  def randomize(self):
    self.val = self.function.execute()
#    print "randomized: PredefinedFunction val: " + str(self.val)
    return self.val

  def value(self):
    return self.val

  def __str__(self):
    return "PredefinedFunction("+str(self.value())+")"

class Variable:
  function = None
  val = None

  def __init__(self, name):
    self.name = name

  def randomize(self):
    self.val = self.function.randomize()
#    print "randomized: Variable " + self.name + " val: " + str(self.val) + " from " + str(self.function)

  def value(self):
    return self.val

  def __str__(self):
    if type(self.value()) == int:
      value = str(self.value())
    else:
      value = "'" + str(self.value()) + "'"
    return "'" + self.name + "':" + value

class Exercice:
  def __init__(self, id, description_list, statements, formula, result):
    self.id = id
    self.resolved_description_list = self.resolve_variables(description_list, statements)
    self.statements = statements
    self.formula = formula
    self.result = result

  def resolve_variables(self, description_list, statements):
    '''Make sure we find the variables'''
    return [ self.resolve_if_necessary(elt, statements) for elt in description_list]

  def resolve_if_necessary(self, elt, statements):
    if (type(elt) == str):
      return elt
    else:
      statement = find(statements, lambda s : s.name == elt.name)
      if (statement == None):
        raise MyException("Unable to resolve variable with name " + s.name)
      return str(statement.value())

  def description(self):
#    converted = [ self.description_text(elt) for elt in self.description_list ]
#    print converted
#    return "\n".join(converted)
    return "".join(self.resolved_description_list)

#  def description_text(self, elt):
#    if (type(elt) == str):
#      return elt
#    else:
#      return elt.value()

  def parse(self, text, displayUnusedVars=False):
    load()
    formulaParser = calc.Calc()
    for s in self.statements:
      formulaParser.names[s.name] = s.value()

    result = formulaParser.parse(text)
    if displayUnusedVars:
      formulaParser.print_unused_vars()
#    print "====== parsing: " + text + " into " + str(type(result)) + " " + str(result)
    del formulaParser
    return result
 
  def generate(self):
    print "Generating: [" + self.id + "]: " + str(self.description())
    for s in self.statements:
      print str(s)
    print "Formula: " + self.formula
    print "Result: " + self.result
    print "Evaluated Formula: " + self.toText(nodeResultEvaluator.visit(self.parse(self.formula, True)))
    print "Evaluated Result: " + self.toText(nodeResultEvaluator.visit(self.parse(self.result)))

  def randomize(self):
#    print "randomize: Exercise"
    for s in self.statements:
      s.randomize()


  def generateLatex(self):
    s = ""
    s += "\\begin{oppgave} " + self.id + " " + str(self.description())
    s += " \\[ "
    s += nodeLatexConvertor.visit(nodeResultEvaluator.visit(self.parse(self.formula, True)))
    s += " \\] "
    s += "\\vspace{-5mm}"
    s += "\\end{oppgave}"
    return s

  def generateLatexResult(self):
    s = ""
    s += "\\begin{result} " + self.id + " " 
    result = nodeLatexConvertor.visit(nodeResultEvaluator.visit(self.parse(self.result)))
    if (result[0] == '"'):
      s += "\\[\\textrm{"
      s += unquoteTEXT(result)
      s += "}\\]"
    else:
      s += "\\["
      s += result
      s += "\\]"
    s += "\\vspace{-5mm}"
    s += "\\end{result}"
    return s

  def toPrettyXml(self, node):
    return prettyPrintXMLTxt(nodeXmlConvertor.visit(node))

  def toText(self, node):
    return formulaTextOutput.visit(node)

  def __str__(self):
    s = "[" + self.id + "]: " + str(self.description()) + "\n"
    for statement in self.statements:
      s += str(statement) + ",\n"
    s += "Formula: " + self.formula + "\n"
    s += "Result: " + self.result + "\n"
    return s

def p_exercise(p):
  'exercise : id description statements formula result'
#  print "exo"
  p[0] = Exercice(p[1], p[2], p[3], p[4], p[5])

def p_exercise_id(p):
  'id : ID'
  p[0] = p[1]

def unquoteTEXT(text):
  pattern = re.compile(r'"(.*)"')
  return pattern.search(text).groups()[0]

def removeSYMBOL(text):
  return text.split(None, 1)[1].strip()

def p_description(p):
  '''description : description AND description_elt
                 | description_elt'''
  if (type(p[1]) == list):
    p[0] = p[1] + [ p[3] ]
  else:
    p[0] = [ p[1] ]

def p_description_elt(p):
  '''description_elt : description_text
                     | description_var'''
  p[0] = p[1]

def p_description_text(p):
  '''description_text : TEXT'''
  p[0] = unquoteTEXT(p[1])

def p_description_var(p):
  '''description_var : VAR'''
  p[0] = Variable(p[1])

def p_statements(p):
  '''statements : 
          | statement
          | statements statement '''
#  print "** statements"
  s = []
  for i in range(1, len(p)):
    s += p[i]
  p[0] = s

def p_statement(p):
  'statement : statement_decl statement_assignment'
#  print "** statement"
  variables = []
  for var in p[1]:
    var.function = p[2]
    var.randomize()
#    print type(var)
  variables += p[1]
  p[0] = variables

def p_statement_decl(p):
  '''statement_decl : statement_decl COMMA VAR
              | VAR'''
  if (type(p[1]) == list):
    p[0] = p[1] + [ Variable(p[3]) ]
  else:
    p[0] = [ Variable(p[1]) ]

def p_statement_assignment(p):
  '''statement_assignment : value_assignment
                          | function_assignment'''
#  print "** statement_decl"
  p[0] = p[1]


def p_value_assignment(p):
  '''value_assignment : decimal_range
                      | int_range
                      | constant
                      | list'''
  p[0] = p[1]

def p_constant(p):
  '''constant : number_or_decimal'''
  p[0] = Constant(p[1])

def p_number_or_decimal(p):
  '''number_or_decimal : DECIMAL
                       | NUMBER'''
  p[0] = p[1]

def p_decimal_range(p):
  '''decimal_range : FUNC_DECIMAL LPAREN number SEMICOLON number RPAREN
                   | FUNC_DECIMAL LPAREN number SEMICOLON number RPAREN BACKSLASH number'''
#  print len(p)
  if (len(p) == 7):
    p[0] = DecimalRange(p[3], p[5])
  else:
    p[0] = DecimalRange(p[3], p[5], p[8])

def p_int_range(p):
  '''int_range : LPAREN number SEMICOLON number RPAREN
               | LPAREN number SEMICOLON number RPAREN BACKSLASH number'''
#  print len(p)
  if (len(p) == 6):
    p[0] = Range(p[2], p[4])
  else:
    p[0] = Range(p[2], p[4], p[7])

def p_list(p):
  '''list : LPAREN number_list RPAREN
          | LPAREN letter_list RPAREN'''
  p[0] = List(p[2])

def p_number_list(p):
  '''number_list : number_list COMMA number
               | number'''
  if (type(p[1]) == list):
    p[0] = p[1] + [ p[3] ]
  else:
    p[0] = [ p[1] ]

def p_letter_list(p):
  '''letter_list : letter_list COMMA letter
                 | letter'''
  if (type(p[1]) == list):
    p[0] = p[1] + [ p[3] ]
  else:
    p[0] = [ p[1] ]

def p_letter(p):
  '''letter : VAR'''
  p[0] = p[1]

def p_function_assignment(p):
  '''function_assignment : FUNC_SIGNALL
                         | FUNC_SIGN1
                         | FUNC_SIGN2'''
#                         | FUNC_SIGN3'''
  p[0] = PredefinedFunction(p[1])  

def p_number(p):
  '''number : NUMBER'''
#  print "** number " + str(p[1])
  p[0] = p[1]

def p_formula(p):
  'formula : SOLVE'
  p[0] = removeSYMBOL(p[1])

def p_result(p):
  'result : SOLUTION'
  p[0] = removeSYMBOL(p[1])

#def p_line_sep(p):
#  'line_sep : LINE_SEP EOL'
#  print "** line_sep"

# Error rule for syntax errors
def p_error(p):
  if p:
    sys.stderr.write("Syntax error at '%s'\n" % p.value)
    raise MyException("Syntax error at '%s'" % p.value)
  else:
    sys.stderr.write("Syntax error at EOF\n")
    raise MyException("Syntax error at EOF")

def parseExo(lines):
  # Build the parser
  import ply.yacc as yacc
  import os
  try:
    modname = os.path.split(os.path.splitext(__file__)[0])[1]
  except:
    modname = "parser"+"_"+"exoparse"
    raise 
#  self.debugfile = modname + ".dbg"
  tabmodule = modname + "_" + "parsetab"

  parser = yacc.yacc(tabmodule=tabmodule)
#  print parser
#  print "========= PARSING EXO"
#  print lines
#  print "========="
  exoLexer = lex.lex(reflags=re.UNICODE)
  r = parser.parse(lines, lexer=exoLexer)
  del exoLexer
  return r

if __name__ == "__main__":
  lines = ""
  while True:
    try:
      line = raw_input()
    except EOFError:
      break
    if not line: continue
    lines += line + "\n"

  #print "\n" + lines
  result = parseExo(lines)
  #print result
  result.generate()
