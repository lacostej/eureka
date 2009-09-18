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
  sys.stderr.write("Syntax error in input! '%s'\n" % str(p))
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

def parseExosLatex(exercises):
  header = '''
\\documentclass[12pt, norsk, a4paper]{article}
\\usepackage{babel, amssymb, amsthm,enumitem, amsmath}
\\usepackage[pdftex]{graphicx}
\\usepackage[latin1]{inputenc}
\\addtolength{\\parskip}{\\baselineskip}
\\theoremstyle{definition}
\\newtheorem{oppgave}{Oppgave}
\\renewcommand{\\labelenumi}{\\alph{enumi})}
\\setlength\\topmargin{0cm}

\\newcommand{\\vek}[2]{\\overrightarrow{#1#2}}
\\newcommand{\\vecc}[1]{\\vec{\\bf #1}}

\\begin{document}

\\begin{flushleft}
\\textsc{Tid:} 90 minutter\\\\[0.8cm]
\\textsc{Hjelpemidler:} Egenproduserte rammenotater\\\\[0.8cm]
\\textsc{Alle svar maa begrunnes}\\\\[1.5cm]
\\end{flushleft}
'''
  footer = '''
\\noindent SLUTT

\\end{document}
'''

  print header
  import exoparse
  for r in exercises:
    exercise = exoparse.parseExo(r.text+"\n")
    if not exercise:
      sys.stderr.write("ERROR: couldn't parse exercise. Skipping\n")
    else:
      print exercise.generateLatex()
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
