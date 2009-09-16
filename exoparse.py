#!/usr/bin/python

# Get the token map from the lexer.  This is required.
from exolex import *

# Build the lexer
import ply.lex as lex
import re
lex.lex(reflags=re.UNICODE)

class Executor:
  def __init__(self, function, param):
    self.function = function
    self.param = param

  def execute(self):
    return self.function(self.param)

class Func:
  pass

def randomFrom(array):
  import random
  return array[random.randint(0, len(array) -1 )]

class List(Func):
  val = None

  def __init__(self, values):
    self.values = values

  def execute(self):
    return randomFrom(self.values)

  def value(self):
    if (self.val == None):
      self.val = str(self.execute())
    return self.val

  def __str__(self):
    return str(self.value())

class Range(Func):
  val = None
  def __init__(self, start, stop, exclude=None):
    self.start = start
    self.stop = stop
    self.exclude = exclude

  def execute(self):
    theRange = range(self.start, self.stop)
    if (self.exclude != None):
      theRange.remove(self.exclude)
    r = randomFrom(theRange)
    return r

  def value(self):
    if (self.val == None):
      self.val = str(self.execute())
    return self.val

  def __str__(self):
#    return "Range("+str(self.start)+","+str(self.stop)+")"
    return "Range(" + self.value() + ")"

class DecimalRange(Func):
  val = None

  def __init__(self, start, stop, exclude=None):
    self.start = start
    self.stop = stop
    self.exclude = exclude

  def execute(self):
    import random
    import decimal
    intr = 0
    while (intr == 0):
      intr = random.randint(self.start * 100, self.stop * 100)
    value=decimal.Decimal(intr)/100
    return value

  def value(self):
    if (self.val == None):
      self.val = str(self.execute())
    return self.val

  def __str__(self):
#    return "Range("+str(self.start)+","+str(self.stop)+")"
    return str(self.value())

signOps=['+','-',':','*']
sign1Ops=['+', '-']
sign2Ops=['*', ':']

class PredefinedFunction(Func):
  val = None
  def __init__(self, func_symbol):
    self.functions = { #Built in Function table
      '\sign' : Executor(randomFrom, signOps),
      '\sign1' : Executor(randomFrom, sign1Ops),
      '\sign2' : Executor(randomFrom, sign2Ops)
    }
    self.function = self.functions[func_symbol]

  def execute(self):
    return self.function.execute()

  def value(self):
    if (self.val == None):
      self.val = str(self.execute())
    return self.val

  def __str__(self):
    return "Range("+self.value()+")"

class Variable:
  function = None
  val = None

  def __init__(self, name):
    self.name = name

  def compute(self):
    self.val = str(self.function.execute())

  def value(self):
    return self.val

  def __str__(self):
    return "var " + self.name + ":" + self.value()

class Exercice:
  def __init__(self, description, statements, formula, result):
    self.description = description
    self.statements = statements
    self.formula = formula
    self.result = result

  def dirty_replace(self, text):
    '''temporary function until we implement formual and solution parsing'''
    for s in self.statements:
      if  (text[0] == s.name):
        text = self.myreplace(text, s.name + " ", s.value() + " ", 1)
      text = self.myreplace(text, "(" + s.name, "(" + s.value() )
      text = self.myreplace(text, s.name + ")", s.value() + ")" )
      text = self.myreplace(text, "{" + s.name, "{" + s.value() )
      text = self.myreplace(text, s.name + "}", s.value() + "}" )
      text = self.myreplace(text, " " + s.name, " " + s.value())
      text = self.myreplace(text, "*" + s.name, "*" + s.value())
      text = self.myreplace(text, "^" + s.name, "^" + s.value())
      text = self.myreplace(text, "=" + s.name, "=" + s.value())
      text = self.myreplace(text, "-" + s.name, "-" + s.value())
      text = self.myreplace(text, "+" + s.name, "+" + s.value())
      text = self.myreplace(text, ":" + s.name, ":" + s.value())
    return text

  def myreplace(self, text, old, new, count=None):
    if (count != None):
      v = text.replace(old, new, count)
    else:
      v = text.replace(old, new)
#    print "replace " + old + " " + new + " " + v
    return v

  def generate(self):
    print "Generating: " + str(self.description)
    for s in self.statements:
      print str(s)
    print "Formula: " + self.dirty_replace(self.formula)
    print "Result: " + self.dirty_replace(self.result)


def p_exercise(p):
  'exercise : description statements formula result'
  p[0] = Exercice(p[1], p[2], p[3], p[4])

def unquoteTEXT(text):
  pattern = re.compile(r'"(.*)"')
  return pattern.search(text).groups()[0]

def removeSYMBOL(text):
  return text.split(None, 1)[1].strip()

def p_description(p):
  'description : TEXT'
  p[0] = unquoteTEXT(p[1])

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
    var.compute()
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
                      | list'''
  p[0] = p[1]

def p_decimal_range(p):
  '''decimal_range : DECIMAL LPAREN number SEMICOLON number RPAREN
                   | DECIMAL LPAREN number SEMICOLON number RPAREN BACKSLASH number'''
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
  print "Syntax error in input! " + str(p)
#  tok = yacc.token()             # Get the next token
#  yacc.errok()

def toto():
# Read ahead looking for a closing '---'
  while 1:
    tok = yacc.token()             # Get the next token
    print tok
    if not tok or tok.type == 'LINE_SEP': break
  if tok and tok.type == "LINE_SEP": print "Found LINE_SEP"
  yacc.restart()

def parseExo(lines):
  # Build the parser
  import ply.yacc as yacc
  parser = yacc.yacc(tabmodule="exo")
  return parser.parse(lines)

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
