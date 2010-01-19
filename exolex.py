#!/usr/bin/python

import ply.lex as lex
import re
import decimal

tokens=(
  'ID',
  'TEXT',
  'AND',
  'FUNC_SIGNALL',
  'FUNC_SIGN1',
  'FUNC_SIGN2',
#  'FUNC_SIGN3',
  'SOLVE',
  'SOLUTION',
  'FUNC_DECIMAL',
  'DECIMAL',
  'NUMBER',
  'BACKSLASH',
  'COMMA',
  'SEMICOLON',
  'LPAREN',
  'RPAREN',
  'VAR'
)

def t_SOLVE(t):
 r'solve .+'
 return t

def t_SOLUTION(t):
 r'solution .+'
 return t

t_TEXT=r'"[^\"]+"'
t_FUNC_SIGNALL=r'\\sign'
t_FUNC_SIGN1=r'\\sign1'
t_FUNC_SIGN2=r'\\sign2'
#t_FUNC_SIGN3=r'\\sign3'
t_FUNC_DECIMAL=r'\\d'
t_BACKSLASH=r'\\'
t_COMMA=r','
t_SEMICOLON=r';'
t_LPAREN='\('
t_RPAREN='\)'
t_VAR=r'[_a-zA-Z]+'
t_AND=r'&'

# A regular expression rule with some action code
def t_DECIMAL(t):
    r'-?\d+\.\d+'
    t.value = decimal.Decimal(t.value)
    return t

def t_ID(t):
    r'id\d+'
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#    print "***"

# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

if __name__ == "__main__":
  # Build the lexer
  lexer = lex.lex(reflags=re.UNICODE)

  import sys
  if (len(sys.argv) > 1):
    # Test it out
    f = open(sys.argv[1], 'r')
    data=f.read()
  else:
    data = ""
    while 1:
      try:
        s = raw_input('calc > ')
      except EOFError:
        break
      if not s: continue
      data += s + "\n"

  # Give the lexer some input
  lexer.input(data)

  # Tokenize
  while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
