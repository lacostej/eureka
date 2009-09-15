#!/usr/bin/python

import ply.lex as lex
import re

tokens=(
  'COMMENT',
  'CAT_LINE',
  'LINE_SEP',
  'EXERCISE_LINE',
)

t_COMMENT=r'\#.*'
t_CAT_LINE=r'\\cat .+'
t_LINE_SEP=r'---'
t_EXERCISE_LINE=r'.+'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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

  # Test it out
  f = open('oppgaver4.txt', 'r')
  data=f.read()

  # Give the lexer some input
  lexer.input(data)

  # Tokenize
  while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
