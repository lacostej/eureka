#!/usr/bin/python

import ply.lex as lex
import re

tokens=(
  'TEXT',
#  'VARNAME',
#  'RESSYMBOL',
  'FUNC_SIGNALL',
  'FUNC_SIGN1',
  'FUNC_SIGN2',
  'SOLVE',
  'SOLUTION',
#  'PLUS',
#  'MINUS',
#  'MULTIPLY',
#  'DIVIDE',
#  'POWER',
  'NUMBER',
  'COMMA',
#  'EQUAL',
  'SEMICOLON',
  'LPAREN',
  'RPAREN',
#  'LBRACE',
#  'RBRACE',
  'VAR'
)

t_TEXT=r'".+"'
#t_RESSYMBOL=r'\\res'
t_FUNC_SIGNALL=r'\\sign'
t_FUNC_SIGN1=r'\\sign1'
t_FUNC_SIGN2=r'\\sign2'
t_SOLVE=r'\\solve .+'
t_SOLUTION=r'\\solution .+'
#t_PLUS=r'\+'
#t_MINUS=r'\-'
#t_MULTIPLY=r'\*'
#t_DIVIDE=r'\\'
#t_POWER=r'\^'
##t_NUMBER=r'\d+'
t_COMMA=r','
#t_EQUAL=r'='
t_SEMICOLON=r';'
t_LPAREN='\('
t_RPAREN='\)'
#t_LBRACE='{'
#t_RBRACE='}'
t_VAR=r'[a-z]'

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

  # Test it out
  f = open('exo1.txt', 'r')
  data=f.read()

  # Give the lexer some input
  lexer.input(data)

  # Tokenize
  while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
