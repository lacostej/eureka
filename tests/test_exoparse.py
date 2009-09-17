import exoparse
import mathparse
import calc

#import urlparse
#import httplib2
#import os
#from email import message_from_string, message_from_file

from decimal import*

TEST_DATA_DIR = "./tests/data/"

nodeResultEvaluator = calc.NodeResultEvaluator()
formulaTextOutput = calc.NodeFormulaSimpleOuptutGenerator()

def setUp(self):
  pass

def tearDown(self):
  pass

def testReadOneExercise():
  text = '''
"l1: addisjon og substraksjon med negative tall. Regn ut"
a (-1;10)
b (-10,-1,-2)
s \\sign1
\\solve a s (b)
\\solution \\res {a s (b)}
'''
  print text

  e = exoparse.parseExo(text)

  assert e.description == "l1: addisjon og substraksjon med negative tall. Regn ut"
  assert len(e.statements) == 3
  assert e.statements[0].name == 'a'
  assert e.statements[0].value() in range(-1, 10)
  assert e.statements[1].name == 'b'
  assert e.statements[1].value() in [-10, -1, -2]
  assert e.statements[2].name == 's'
  assert e.statements[2].value() in ['*',':','+','-']
  assert e.formula == "a s (b)"
  assert e.result == "\\res {a s (b)}"

  e.generate()
#def testXxxy():
#  assert False


def test_fullLoad():
  f = open('data/oppgaver4.txt', 'r')
  lines = f.read()
  exercises = mathparse.parseFile(lines)
  mathparse.parseExos(exercises)


def testCurrentlyFailingExercice():
  ''' usefull during development, place the failing exercice in failing.txt and uncomment'''
  f = open('failing.txt', 'r')
  text = f.read()
  e = exoparse.parseExo(text)
  e.generate()

def atestMultipleSolutions():
  f = open('data/multiple_solutions.txt', 'r')
  text = f.read()
  e = exoparse.parseExo(text)
  e.generate()

def testEvaluateSimpleOperators():
  v = { "a": 6,
       "b": 9,
       "e": -5,
       "f": -10,
       "g": -10,
       "s": ':',
       "t": ':',
       "u": '*',
       "v": ':'
     }
  evaluation = evaluate(v, "\\res { a s (e) t b u (f) v (g)}")
  assert formulaTextOutput.visit(evaluation) == "-10.8"

def testEvaluatePowersAndStandardForm():
  v = { "a": Decimal("7.02"),
       "b": -7,
       "c": Decimal("8.54"),
       "d": -4,
       "s": ':'
     }
  evaluation = evaluate(v, "\\stdform {\\res { a*10^b s c*10^d}}")
  s = formulaTextOutput.visit(evaluation)
  print s
  assert s == "0.0008220140515222482435597189696"

def testOperationsFractions():
  v = {
    "a": 3,
    "b": 7,
    "c": 1,
    "d": 4,
    "e": 1,
    "f": 1,
    "u": '+',
    "v": '-'
  }
  evaluation = evaluate(v, "\\res {\\frac {a}{b} u \\frac {c}{d} v \\frac {e}{f}}")
  s = formulaTextOutput.visit(evaluation)
  print s
  assert s  == "-9/28"

def testOperationsFractions():
  v = {
    "a": 3,
    "b": 7,
    "c": 1,
    "d": 4,
    "e": 1,
    "f": 5,
    "u": '*',
    "v": ':'
  }
  evaluation = evaluate(v, "\\res {\\frac {a}{b} u \\frac {c}{d} v \\frac {e}{f}}")
  s = formulaTextOutput.visit(evaluation)
  print s
  assert s  == "15/28"


def evaluate(variables, formula):
  formulaParser = calc.Calc()
  for s in variables:
    formulaParser.names[s] = variables[s]

  result = formulaParser.parse(formula)
  print result
  evaluation = nodeResultEvaluator.visit(result)
  print "eval " + str(evaluation)
  return evaluation


def testFormatNumber():
  s = formulaTextOutput.formatNumber(Decimal("-10.800000000000"))
  print s
  assert s == "-10.8"


#def testDecimalPower():
#  import decimal
#  print "-------------------"
#  print decimal.getcontext().power(decimal.Decimal("3.8"), decimal.Decimal("2.4") )
#  print decimal.getcontext().power(decimal.Decimal(3), decimal.Decimal(4) )

#def testXxx():
#  decimal.
