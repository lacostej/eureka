#!/usr/bin/python

import sys

# Get the token map from the lexer.  This is required.
from mathlex import *

# Build the lexer
import ply.lex as lex
import re
fileLexer = lex.lex(reflags=re.UNICODE)

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
  # Build the parser
  import ply.yacc as yacc
  parser = yacc.yacc(tabmodule="mathparse_parsetab")

  #print "\n" + text
  return parser.parse(text, lexer=fileLexer)

def parseExos(exercises):
  import exoparse
  for r in exercises:
    print "---"
    print r
#    print "---"
#    print r.text
    exercise = exoparse.parseExo(r.text+"\n")
    if not exercise:
      print "ERROR: couldn't parse exercise. Skipping"
    else:
      exercise.generate()

def generateLatexExercisesForStudent(exercises, dir, outputFileName, student, studentData):
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
\\textsc{Tid:} 90 minutter\\\\[0.8cm]
\\textsc{Hjelpemidler:} Egenproduserte rammenotater\\\\[0.8cm]
\\textsc{Alle svar maa begrunnes}\\\\[1.5cm]
\\end{flushleft}
'''
  middle = '''
\\newtheorem{result}{Resultat}
'''

  footer = '''
\\noindent SLUTT

\\end{document}
'''

  output = open(outputFileName, "w")

  exos = []
  import exoparse
  for r in exercises:
    exercise = exoparse.parseExo(r.text+"\n")
    if not exercise:
      sys.stderr.write("ERROR: couldn't parse exercise. Skipping\n")
    else:
#      print "generated " + exercise
      exos.append(exercise)

  output.write(header + "\n")

  if (studentData.comment != None and len(studentData.comment) > 0):
    comment = studentData.comment.encode("iso-8859-15")
    # FIXME encode Norwegian characters appropriately
    output.write("\\begin{flushleft}\n")
    output.write("\\textsc{Oppgave:} " + studentData.comment.encode("iso-8859-15") + "\\\\[1.2cm]\n")
    output.write("\\end{flushleft}\n")

  for exoId in studentData.exerciseStatuses.iterkeys():
#    print exoId
    exoData = studentData.exerciseStatuses[exoId]
    if (exoData == None):
      raise MyException("no data for " + exoId + " for student " + student.shortName)
    if (exoData.toGenerate > 0):
      exo = find(exos, lambda e: e.id == exoId)
      if (exo == None):
        continue
#        raise MyException("Unknown exercise: " + exoId)
      for i in range(exoData.toGenerate):
        output.write(exo.generateLatex() + "\n")

  output.write(footer + "\n")  

def parseExosLatex(exercises):
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
\\textsc{Tid:} 90 minutter\\\\[0.8cm]
\\textsc{Hjelpemidler:} Egenproduserte rammenotater\\\\[0.8cm]
\\textsc{Alle svar maa begrunnes}\\\\[1.5cm]
\\end{flushleft}
'''
  middle = '''
\\newtheorem{result}{Resultat}
'''

  footer = '''
\\noindent SLUTT

\\end{document}
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

  print header
  for e in exos:
    print e.generateLatex()
  print middle
  for e in exos:
    print e.generateLatexResult()
  print footer

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
