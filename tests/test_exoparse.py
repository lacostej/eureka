import exoparse
import mathparse
import calc

#import urlparse
#import httplib2
#import os
#from email import message_from_string, message_from_file

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

def testMultipleSolutions():
  f = open('data/multiple_solutions.txt', 'r')
  text = f.read()
  e = exoparse.parseExo(text)
  e.generate()

def testEvaluate():
#  f = open('data/multiple_solutions.txt', 'r')
#  text = f.read()
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

  formulaParser = calc.Calc()
  for s in v:
    formulaParser.names[s] = v[s]

  result = formulaParser.parse("\\res { a s (e) t b u (f) v (g)}")
  print result

  evaluation = nodeResultEvaluator.visit(result)
  print evaluation
  assert formulaTextOutput.visit(evaluation) == "-10.8"
#e.generate()

