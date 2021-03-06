import exoparse
import mathparse
import calc

#import urlparse
#import httplib2
#import os
#from email import message_from_string, message_from_file

from decimal import *
from utils import *
from assert_utils import *

TEST_DATA_DIR = "data/"

nodeResultEvaluator = calc.NodeResultEvaluator()
formulaTextOutput = calc.NodeFormulaSimpleOuptutGenerator()
nodeLatexConvertor = calc.NodeLatexConvertor()

def setUp(self):
  pass

def tearDown(self):
  pass

def testReadOneExercise():
  text = '''
id0
"l1: addisjon og substraksjon med negative tall. Regn ut"
a (-1;10)
b (-10,-1,-2)
s \\sign1
solve a s (b)
solution \\res {a s (b)}
'''
  print text

  e = exoparse.parseExo(text)

  print list_str(e.statements)

  assertEquals(e.description(), "l1: addisjon og substraksjon med negative tall. Regn ut")
  assert len(e.statements) == 3
  assert e.statements[0].name == 'a'
  assert e.statements[0].value() in range(-1, 11)
  assert e.statements[1].name == 'b'
  assert e.statements[1].value() in [-10, -1, -2]
  assert e.statements[2].name == 's'
  assert e.statements[2].value() in ['*',':','+','-']
  assert e.formula == "a s (b)"
  assert e.result == "\\res {a s (b)}"

  e.generate()
#def testXxxy():
#  assert False

def testReRandomizeWorks():
  text = '''
id0
"l1: addisjon og substraksjon med negative tall. Regn ut"
a (-1000;1000)
b (-1000;1000)
s \\sign1
solve a s (b)
solution \\res {a s (b)}
'''
  print text

  e = exoparse.parseExo(text)
  #e.generate()
  a1 = e.statements[0].value()
  e.randomize()
  a2 = e.statements[0].value()
  #e.generate()
  assertNotEquals(a1, a2)

def test_fullLoad():
  lines = _dataread('oppgaver4.txt')
  exercises = mathparse.parseFile(lines)
  mathparse.parseExos(exercises)

def testCurrentlyFailingExercice():
  ''' usefull during development, place the failing exercice in failing.txt and uncomment'''
  text = _dataread('failing.txt')
  e = exoparse.parseExo(text)
  e.generate()
#  assert False

def testMultipleSolutions():
  '''Here we just fully convert all our exercises to see if we don't have a big error'''
  text = _dataread('multiple_solutions.txt')
  e = exoparse.parseExo(text)
  e.generate()

def test_id4_1():
  assertEvaluationRenders({}, "\\res {(1 - (-10) * 3) * -8 + (-8) : (-5)}", "-246.4")

def test_id5_1_result():
  v = {
"a":2,
"b":2,
"e":-2,
"f":-3,
"g":-3,
"h":-3,
"j":-3,
"i":2,
"s":':',
"t":'+',
"u":'-',
"v":'+',
"w":'*',
  }
#  assertEvaluationRenders(v, "\\res { (a s (e) t b)*(h) u ((f) v (g))^i w (j)}", "105")

def test_id5_2_result():
  assertEvaluationRenders({}, "\\res { (2 : (-2) + 2)*(-3) - ((-3) + (-3))^2 * (-3)}", "105")

def test_id5_3_result():
  v = {
"a":2,
"b":2,
"e":-2,
"s":':',
"t":'+',
  }
  assertEvaluationRenders(v, "\\res { (a s (e) t b)}", "1")

def test_id5_3bis_result():
  v = {
"a":2,
"b":2,
"e":2,
"s":':',
"t":'-',
  }
  assertEvaluationRenders(v, "\\res { a s e - b }", "-1")

def test_id5_4_result():
  assertEvaluationRenders({}, "\\res { (2 : (-2) + 2)}", "1")

def testEvaluateSimpleOperators_id4_2():
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
  assertEvaluationRenders(v, "\\res { a s (e) t b u (f) v (g)}", "-0.13")

def test_id5_1():
  assertEvaluationRenders({}, "\\res { (2 : (-4) + 2)*-5 : ((-6) + (-2))^2 + -9}", "-9.12")

def testEvaluatePrecedenceOfMultiplicationAndDivisionWithoutParentheses():
  assertEvaluationRenders({ }, "\\res { 2 : -1 * -2 }", "4")

def testEvaluatePrecedenceOfMultiplicationAndDivisionWhenParentheses1():
  assertEvaluationRenders({ }, "\\res { (-2) : 1 * (-2) }", "4")

def testEvaluatePrecedenceOfMultiplicationAndDivisionWhenParentheses2():
  assertEvaluationRenders({ }, "\\res { 2 : (-1) * (-2) }", "4")

def testEvaluatePrecedenceOfMultiplicationAndDivisionWhenParentheses_id2_1():
  assertEvaluationRenders({ }, "\\res { 6 * (-3) * 7 : (-5) * (-8)}", "-201.6")

def test_id16():
  assertEvaluationRenders({ }, "10^\\res{2*3*4}", "10^24")

def testVarAsConstants():
  text = _dataread("exo_constants.txt")
  e = exoparse.parseExo(text)
  assertEquals("l1: demonstrate use of 2 types of constants: -2.5", e.description())
  s = e.generateLatexResult()
  assertEquals("\\begin{result} id4 \[5\]\\vspace{-5mm}\end{result}", s)

def test_operations_latex():
  v = {
    "a": "a",
  }
  assertEvaluationLatexRenders(v, "3 * a", "3 \cdot a")

def testEvaluatePowersAndStandardForm():
  v = { "a": Decimal("7.02"),
       "b": -7,
       "c": Decimal("8.54"),
       "d": -4,
       "s": ':'
     }
  assertEvaluationRenders(v, "\\stdform {\\res { a*10^b s c*10^d}}", "8.22 * 10^-12")

def testEqualIsATopLevelFormulaElement():
  v = {
    "a": "a",
  }
  e = evaluate(v, "3^4=a")
  assertEquals(str(e), "Node: equals,(Node: ^,(3,4),Node: var,(a))")  

def test_id31():
  v = {
    "a": 5,
    "b": 4,
    "c": 8,
    "x": "x",
  }
  e = evaluate(v, "a*x - b = c")
  assertEvaluationRenders(v, "a*x - b = c", "5 * x - 4 = 8")
  assertEvaluationRenders(v, "\\res{(c+b):a}", "2.4")


def test_id109():
  v = {
   "a": 2,
   "c": 2,
   "d": 2,
   "e": 2,
   "b": 10
  }
  e = evaluate(v, "\\frac {\\sqrt {a}  {\\res {b^a}} * \\sqrt {c}  {\\res {b^a} ^d}} { \\res {b^a}^e * \\sqrt {c}  {\\res {b^a} ^e}}")
  assertEquals(str(nodeLatexConvertor.visit(e)), "\\frac{\\sqrt[2]{100} \\cdot \\sqrt[2]{100^{2}}}{100^{2} \\cdot \\sqrt[2]{100^{2}}}")

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
  assertEvaluationRenders(v, "\\res {\\frac {a}{b} u \\frac {c}{d} v \\frac {e}{f}}", "-9/28")

def testOperationsFractions_2():
  v = {
    "a": 5,
    "b": 5,
    "c": 5,
    "d": 5,
    "e": 5,
    "f": 3,
    "u": '+',
    "v": '+'
  }
  assertEvaluationRenders(v, "\\res {\\frac {a}{b} u \\frac {c}{d} v \\frac {e}{f}}", "11/3")

def testOperationsFractions_3():
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
  assertEvaluationRenders(v, "\\res {\\frac {a}{b} u \\frac {c}{d} v \\frac {e}{f}}", "15/28")

def testOperationsFractions_id118_2():
  v = {
    "a": 4,
    "b": 2,
    "c": 2,
    "d": 8,
    "e": 4,
    "f": 1,
    "u": '-',
  }
  assertEvaluationRenders(v, "\\res {(\\frac {a}{b} u \\frac {c}{d}) * \\frac {e}{f}}", "7")

def testOperationsFractions_id121():
  v = {
    "a": -5,
    "b": -3,
    "c": -3,
    "d": -4,
    "e": -3,
    "f": -3,
  }
  assertEvaluationRenders(v, "\\res {(\\frac{a}{b} )^c * (\\frac{d}{e} )^f}", "(5/3)^-3 * (4/3)^-3")

def testOperationsFractions_id127():
  v = {
    "a": 3,
    "b": 2,
    "c": 3,
    "d": 3,
    "g": 4,
  }
  assertEvaluationRenders(v, "\\res{\\frac{a-g*c-d}{g*b}}", "-3/2")

def testFormatNumber1():
  assertEquals(calc.formatNumber(Decimal("-10.800000000000")), "-10.8")

def testFormatNumber2():
  assertEquals(calc.formatNumber(Decimal("-9.1171875")), "-9.12")

def testFormatNumber3():
  assertEquals(calc.formatNumber(Decimal("-10.0000")), "-10")

#def testDecimalPower():
#  import decimal
#  print "-------------------"
#  print decimal.getcontext().power(decimal.Decimal("3.8"), decimal.Decimal("2.4") )
#  print decimal.getcontext().power(decimal.Decimal(3), decimal.Decimal(4) )

#def testXxx():
#  decimal.

def testReduceFrac():
  assertFracReduction([2,4], [1,2])

  assertFracReduction([2,5], [2,5])

  assertFracReduction([2*2*2*3*7, 2*3*5*11], [28, 55])

def testReduceFrac2():
  assertFracReduction([12,8], [3,2])
  assertFracReduction([2*2*3*4*5,2*2*3*4*7], [5,7])

def testSplit():
  assertSplit(12, [2,2,3])

def testStdformNegative():
  assertEquals ("8.22 * 10^-4", calc.stdform(Decimal("0.0008221")))

def testStdformNegativeWithRounding():
  assertEquals ("8.23 * 10^-4", calc.stdform(Decimal("0.0008226")))

def testStdformPositive():
  assertEquals ("8.22 * 10^4", calc.stdform(Decimal("82215.6")))

def testStdformInteger():
  assertEquals ("8.22 * 10^4", calc.stdform(82214))

def testStdformLatexInteger():
  assertEquals ("8.22 \cdot 10^{4}", calc.stdformLatex(82214))

def testStdformIntegerRounding():
  assertEquals ("8.23 * 10^4", calc.stdform(82263))

def testStdformIntegerNoExponent():
  assertEquals ("8", calc.stdform(8))

def testStdformDecimalNoExponent():
  assertEquals ("8.22", calc.stdform(Decimal("8.22")))

def testStdformDecimalNoExponentRounding():
  assertEquals ("8.23", calc.stdform(Decimal("8.226")))

def testDecformNegative():
  assertEquals ("0.0001", calc.decform(Decimal("0.0001")))

def testDecform():
  v = {
    "a": -5,
    "b": -3,
  }  
  assertEvaluationLatexRenders(v, "\\res {\\decform {10^a}} : \\res {\\decform {10^b}}", "0.00001 \div 0.001")

def testNegativeSignExtractedOutOfFractions():
  assertEvaluationLatexRenders({}, "\\res {\\frac{-5}{2}}", "-\\frac{5}{2}")

def testTextSolution():
  text = _dataread('example_with_text_solution.txt')
  e = exoparse.parseExo(text)
  s = e.generateLatexResult()
  assertEquals("\\begin{result} id1 \\[\\textrm{FIXME}\\]\\vspace{-5mm}\end{result}", s)

def testParseMultipleLineDescriptions():
  text = _dataread('exo2_multiline_description.txt')
  e = exoparse.parseExo(text)
  assertEquals("l2: this is an exercise with multiline description 1-1 a description that only ends when there are no more lines", e.description())

def testParseMultipleLineDescriptions2():
  text = _dataread('exo_id154.txt')
  e = exoparse.parseExo(text)
  e.generate()
  print e.description()
#  print e.generateLatexResult()
#  assert false

# introduced to detect an issue. to revisit
#def testId154():
#  for a in range(1,11):
#    for b in range(2,11):
#      v = {
#        "a": a,
#        "b": b
#      }
#      formula = "\\res {(1-(a:100))^(-b:2)-1}"
#      evaluation = evaluate(v, formula)
#      if nodeLatexConvertor.visit(evaluation) == "0.29":
#        print "SOLVED with " + str(a) + " " + str(b)
#  assert False

def test_replaceVariables_1():
  v = {
    "a": 2,
    "b": -3,
    "s": '+',
  }
  assertEquals(_replaceVariables(v, "a s (b)"), "2 + (-3)")

########################################################################
### HELPER FUNCTIONS
########################################################################

def _dataread(fileName):
  f = open(TEST_DATA_DIR + fileName, 'r')
  return f.read()

def _replaceVariables(variables, formula):
  formulaParser = calc.Calc()
  for s in variables:
    formulaParser.names[s] = variables[s]
  return formulaParser._replaceVariables(formula)

def evaluate(variables, formula):
  formulaParser = calc.Calc()
  for s in variables:
    formulaParser.names[s] = variables[s]

  result = formulaParser.parse(formula)
  print result
  evaluation = nodeResultEvaluator.visit(result)
  print "eval " + str(evaluation)
  return evaluation

def assertEvaluationRenders(variables, formula, expectedTextResult):
  evaluation = evaluate(variables, formula)
  assertEquals( formulaTextOutput.visit(evaluation), expectedTextResult)

def assertEvaluationLatexRenders(variables, formula, expectedTextResult):
  evaluation = evaluate(variables, formula)
  assertEquals( nodeLatexConvertor.visit(evaluation), expectedTextResult)

def assertFracReduction(frac1, expectedFrac):
  a, b = calc.reduceFrac(frac1[0], frac1[1])
  assertEquals(a, expectedFrac[0])
  assertEquals(b, expectedFrac[1])

def assertSplit(x, expectedSplit):
  y = calc.split(x)
  assertEquals(y, expectedSplit)
