#!/usr/bin/python

# Get the token map from the lexer.  This is required.
from exolex import *

# Build the lexer
import ply.lex as lex
import re
lex.lex(reflags=re.UNICODE)

class Func:
  pass

def randomFrom(array):
  import random
  return array[random.randint(0, len(array) -1 )]

class OneOf(Func):
  def __init__(self, values):
    self.values = values

  def execute(self):
    return randomFrom(self.values)

  def __str__(self):
#    return "OneOf("+",".join(values)+")"
    return str(self.execute())

class Range(Func):
  def __init__(self, start, stop):
    self.start = start
    self.stop = stop

  def execute(self):
    return randomFrom(range(self.start, self.stop))

  def __str__(self):
#    return "Range("+str(self.start)+","+str(self.stop)+")"
    return str(self.execute())

signOps=['+','-',':','*']
sign1Ops=['+', '-']
sign2Ops=['*', ':']

class PredefinedFunction(Func):
  def __init__(self, func_symbol):
    self.functions = { #Built in Function table
      '\sign' : randomFrom(signOps),
      '\sign1' : randomFrom(sign1Ops),
      '\sign2' : randomFrom(sign2Ops)
    }
    self.function = self.functions[func_symbol]

  def __str__(self):
    return "Range("+str(self.function)+")"

class Variable:
  function = None

  def __init__(self, name):
    self.name = name

  def setFunction(function):
    self.function = function

  def __str__(self):
    return "var " + self.name + ":" + str(self.function)

class Exercice:
  def __init__(self, description, statements, formula, result):
    self.description = description
    self.statements = statements
    self.formula = formula
    self.result = result

  def generate(self):
    print "Generating: " + str(self.description)
    for s in self.statements:
      print str(s)
    print "Formula: " + self.formula
    print "Result: " + self.result


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
  s = []
  for var in p[1]:
    var.function = p[2]
#    print type(var)
  s += p[1]
  p[0] = s

def p_statement_decl(p):
  '''statement_decl : statement_decl COMMA VAR
              | VAR'''
  
  if (type(p[1]) == list):
    p[0] = p[1] + [ Variable(p[3]) ]
  else:
    p[0] = [ Variable(p[1]) ]

def p_statement_assignment(p):
  '''statement_assignment : range
                          | one_of
                          | function_assignment'''
#  print "** statement_decl"
  p[0] = p[1]

def p_range(p):
  'range : LPAREN number SEMICOLON number RPAREN'
  p[0] = Range(p[2], p[4])

def p_one_of(p):
  'one_of : LPAREN number_list RPAREN'
  p[0] = OneOf(p[2])

def p_number_list(p):
  '''number_list : number_list COMMA number
               | number'''
  if (type(p[1]) == list):
    p[0] = p[1] + [ p[3] ]
  else:
    p[0] = [ p[1] ]

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
