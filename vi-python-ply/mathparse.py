#!/usr/bin/python

import sys, traceback
import datetime

# Get the token map from the lexer.  This is required.
from mathlex import *

# Build the lexer
import ply.lex as lex
import re

from utils import *

class Exercise:
  category = None

  def __init__(self, lines):
    self.lines = lines
    self.text = "\n".join(self.lines)

  def __str__(self):
    return self.category + "," + str(len(self.lines)) + " lines"

def p_all(p):
  '''all : category_exercises
         | all category_exercises'''
  if (type(p[1]) == list and len(p) > 2):
    p[0] = p[1] + p[2]
  else:
    p[0] = p[1]

def p_category_exercises(p):
  'category_exercises : cat_title line_sep manyexercises line_sep'
#  cat = cat(p[1])
  for a in p[3]:
    a.category = p[1]
  p[0] = p[3]

def p_cat_title(p):
  'cat_title : CAT_LINE'
  p[0] = removeSYMBOL(p[1])
#  print "\nStarting category " + p[0]
  
def p_line_sep(p):
  'line_sep : LINE_SEP'
#  print "** line_sep"

def p_manyexercise(p):
  '''manyexercises : manyexercises line_sep exercise
                   | exercise'''
  if (type(p[1]) == list):
    p[0] = p[1] + [ p[3] ]
  else:
    p[0] = [ p[1] ]

def p_exercise(p):
  'exercise : exercise_lines'
  p[0] = Exercise(p[1])

def p_exercise_lines(p):
  '''exercise_lines : exercise_lines exercise_line
                    | exercise_line'''
  l = []
  if (type(p[1]) == list):
    l += p[1]
    if (p[2]) != None:
      l.append(p[2])
  else:
    if (p[1]) != None:
      l.append(p[1])
  p[0] = l

def p_exercise_line(p):
  '''exercise_line : EXERCISE_LINE
                   | comment'''
  p[0] = p[1]

def p_comment(p):
  'comment : COMMENT'
  p[0] = None # IGNORED

#def p_description(p):
#  'description : TEXT EOL'
#  print "** desc"

# Error rule for syntax errors
def p_error(p):
  if p:
    sys.stderr.write("Syntax error at '%s'\n" % p.value)
    raise MyException("Syntax error at '%s'" % p.value)
  else:
    sys.stderr.write("Syntax error at EOF\n")
    raise MyException("Syntax error at EOF")
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

def parseFile(text):
  fileLexer = lex.lex(reflags=re.UNICODE)
  # Build the parser
  import ply.yacc as yacc
  parser = yacc.yacc(tabmodule="mathparse_parsetab")

  #print "\n" + text
  r = parser.parse(text, lexer=fileLexer)
  del fileLexer
  del parser
  return r

def parseExos(exercises):
  import exoparse
  for r in exercises:
    print "---"
    print r
#    print "---"
#    print r.text
    try:
      exercise = exoparse.parseExo(r.text+"\n")
      if not exercise:
        print "ERROR: couldn't parse exercise. Skipping"
      else:
        exercise.generate()
    except Exception:
     print "ERROR: failed to generate exercise " + str(r)
     traceback.print_exc()
     raise

def generateLatexExercisesAndResultsForStudent(exercises, sortedExoIDs, dir, exercicesOutputFileName, resultsOutputFileName, student, studentData):
  with open(exercicesOutputFileName, "w") as exosOutput:
    with open(resultsOutputFileName, "w") as resultsOutput:
      _generateLatexExercisesAndResultsForStudentFile(exercises, sortedExoIDs, dir, exosOutput, resultsOutput, student, studentData)

def _generateLatexExercisesAndResultsForStudentFile(exercises, sortedExoIDs, dir, exosOutput, resultsOutput, student, studentData):
  middle = '''
\\newtheorem{result}{Resultat}
'''

  exos = {}
  import exoparse
  for r in exercises:
    exercise = exoparse.parseExo(r.text+"\n")
    if not exercise:
      sys.stderr.write("ERROR: couldn't parse exercise. Skipping\n")
    else:
#      print "generated " + str(exercise)
      exos[exercise.id] = exercise

  now = datetime.datetime.utcnow()
  exosOutput.write(latexHeader(now, student.fullName) + "\n")
  resultsOutput.write(latexHeader(now, student.fullName) + "\n")
  resultsOutput.write(middle + "\n")

  if (studentData.uComment != None and len(studentData.uComment) > 0):
    comment = studentData.uComment.encode("utf-8")
    exosOutput.write("\\begin{flushleft}\n")
    exosOutput.write("\\textsc{Oppgave:} " + comment + "\\\\[1.2cm]\n")
    exosOutput.write("\\end{flushleft}\n")
    resultsOutput.write("\\begin{flushleft}\n")
    resultsOutput.write("\\textsc{Oppgave:} " + comment + "\\\\[1.2cm]\n")
    resultsOutput.write("\\end{flushleft}\n")

  for exoId in sortedExoIDs:
    if (not exos.has_key(exoId)):
      continue
    exo = exos[exoId]
    exoData = studentData.exerciseStatuses[exo.id]
    if (exoData == None):
      raise MyException("no data for " + exo.id + " for student " + student.shortName)
    if (exoData.toGenerate > 0):
#        raise MyException("Unknown exercise: " + exoId)
      for i in range(exoData.toGenerate):
        exo.randomize()
        exosOutput.write(exo.generateLatex() + "\n")
        resultsOutput.write(exo.generateLatexResult() + "\n")

  exosOutput.write(latexFooter() + "\n")
  resultsOutput.write(latexFooter() + "\n")
  exosOutput.close()
  resultsOutput.close()
  exoparse.unload()
  del sys.modules['exoparse']
#  print "________"
#  print sys.modules

def parseExosLatex(exercises):
  middle = '''
\\newtheorem{result}{Resultat}
'''
  exos = []
  import exoparse
  for r in exercises:
    exercise = exoparse.parseExo(r.text+"\n")
    if not exercise:
      sys.stderr.write("ERROR: couldn't parse exercise. Skipping\n")
    else:
#      print "generated " + exercise
      exos.append(exercise)

  now = datetime.datetime.utcnow()
  print latexHeader(now, "N/A")
  for e in exos:
    try:
      print e.generateLatex()
    except Exception:
     print "ERROR: failed to generate exercise " + str(e)
     traceback.print_exc()
     raise
  print middle
  for e in exos:
    try: 
      print e.generateLatexResult()
    except Exception:
     print "ERROR: failed to generate exercise " + str(e)
     traceback.print_exc()
     raise
  print latexFooter()

def latexHeader(date, name):
  header = '''
\\documentclass[12pt, norsk, a4paper]{article}
\\usepackage{babel, amssymb, amsthm,enumitem, amsmath}
\\usepackage[pdftex]{graphicx}
\\usepackage[utf8]{inputenc}
\\theoremstyle{definition}
\\newtheorem{oppgave}{Oppgave}
\\renewcommand{\\labelenumi}{\\alph{enumi})}
\\setlength\\topmargin{0cm}

\\begin{document}

\\begin{flushleft}
\\textsc{Dato:} %s\\\\[0.8cm]
\\textsc{Navn:} %s\\\\[0.8cm]
\\textsc{Hjelpemidler:} Egenproduserte rammenotater\\\\[0.8cm]
\\textsc{Alle svar maa begrunnes}\\\\[1.5cm]
\\end{flushleft}
''' % (date.strftime("%d %b %Y"), name)
  return header

def latexFooter():
  footer = '''
\\noindent SLUTT

\\end{document}
'''
  return footer


if __name__ == "__main__":
  lines = ""
  while True:
    try:
      line = raw_input()
  #       print "**************" + s
    except EOFError:
      break
    if not line: continue
    lines += line + "\n"

  exercises = parseFile(lines)
  parseExosLatex(exercises)
