#!/usr/bin/env python

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
#
# Class-based example contributed to PLY by David McNab
# -----------------------------------------------------------------------------

import sys
#sys.path.insert(0,"../..")

#if sys.version_info[0] >= 3:
#    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os
import decimal
from utils import *
from math_expression import *

class FormulaParser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        self.resolved_vars = []
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        self.formulaLexer = lex.lex(module=self, debug=self.debug)
        self.parser = yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('calc > ')
            except EOFError:
                break
            if not s: continue
            self.parse(s)

    def parse(self, s):
      return self.parser.parse(self._replaceVariables(s), lexer=self.formulaLexer)

    def _replaceVariables(self, s):
      result = []
      i = 0
      inText = False
      text = []
      while True:
        if i < len(s) and ischar(s[i]):
          text.append(s[i])
          inText = True
        else:
          if (len(text) > 0):
            v = "".join(text)
            # FIXME we are also trying to resolve the functions (res, frac, etc...)
            t = self.resolve_var(v)
            result += str(t)
            text = []
          if (i < len(s)):
            result.append(s[i])
          inText = False
        if (i == len(s)):
          break
        i += 1
      result = "".join(result)
#      print "replaced " + s + " into " + result
      return result

    def resolve_var(self, v):
      if (not v in self.resolved_vars):
        self.resolved_vars.append(v)
      try:
        return self.names[v]
      except LookupError:
        return v

    def print_unused_vars(self):
      for v in self.names.keys():
        if (not v in self.resolved_vars):
          print "WARNING: Unused: var: name: " + str(v) + " value: " + str(self.names[v])

toXmlConvertor = NodeXmlConvertor()

class Calc(FormulaParser):
    '''The PLY parser that converts the textual formula/result into a Tree.'''

    tokens = (
        'NUMBER', 'DECIMAL',
        'PLUS','MINUS','POWER','TIMES','DIVIDE','EQUALS', #,'EXP'
        'LPAREN','RPAREN', 'COMMA',
        'LBRACE','RBRACE',
        'VARNAME',
        'OR_SYMBOL','SQRTSYMBOL','RESULTSYMBOL','FRACSYMBOL','STDFORMSYMBOL','DECFORMSYMBOL',
        'TEXT'
        )

    # Tokens

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
#    t_EXP     = r'\*\*'
    t_TIMES   = r'\*'
    t_POWER   = r'\^'
    t_DIVIDE  = r':'
    t_EQUALS  = r'\='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_COMMA   = r','
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
#    t_VARNAME = r'[a-zA-Z]'
    t_RESULTSYMBOL = r'\\res'
    t_FRACSYMBOL = r'\\frac'
    t_SQRTSYMBOL = r'\\sqrt'
    t_STDFORMSYMBOL = r'\\stdform'
    t_DECFORMSYMBOL = r'\\decform'
#    t_OR_SYMBOL = r'eller'
    t_TEXT = r'".+"'

    def t_OR_SYMBOL(self, t):
        r'eller'
        return t

    def t_VARNAME(self, t):
        r'[_a-zA-Z]+'
        return t

    def t_DECIMAL(self, t):
        r'\d+\.\d+'
#        try:
        t.value = decimal.Decimal(t.value)
#        except ValueError:
#          
#            print("Decimal value too large %s" % t.value)
#            t.value = 0
        #print "parsed number %s" % repr(t.value)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        #print "parsed number %s" % repr(t.value)
        return t

#    def t_TEXT(sefl, t):
#        r'.+'
#        return t


    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('left', 'POWER'),
        ('right','UMINUS'),
        )

    def find_var(self, x):
      try:      
        return self.names[x]
      except LookupError:
        sys.stderr.write("Undefined name '%s'\n" % x)
        raise

    start = 'top'

    def p_start(self, p):
      '''top : text
             | multiple_expressions
             | equals
             | list
             | expression'''
      p[0] = p[1]

    def p_expression_text(self, p):
       'text : TEXT'
#       print "*** TEXT"
       p[0] = Node("text", [p[1]])

    def p_expression_list(self, p):
       'list : LPAREN list_inside RPAREN'
       p[0] = Node("list", p[2])

    def p_expression_list_inside(self, p):
      '''list_inside : list_inside COMMA expression
                     | expression'''
      if type(p[1]) == list:
        p[0] = p[1] + [ p[3] ]
      else:
        p[0] = [ p[1] ]

    def p_expression_equals(self, p):
       'equals : expression EQUALS expression'
#       print "*** EQUALS " + str(p[1]) + " = " + str(p[3])
       p[0] = Node("equals", [p[1], p[3]])

    def p_expression_multiple_expressions(self, p):
        'multiple_expressions : VARNAME NUMBER EQUALS expression OR_SYMBOL VARNAME NUMBER EQUALS expression'
        p[0] = Node("eller", [Node("var", [p[1]+str(p[2]), p[4]]), Node("var", [p[6]+str(p[7]), p[9]])])

    def p_expression_binop(self, p):
        """
        expression : expression POWER expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression MINUS expression
                   | expression PLUS expression
        """
        ops = [ '+', '-', '*', ':', '^']
        if not p[2] in ops:
          p[2] = self.find_var(p[2])

#        print "*** " + p[2] + " " + str(p[1]) + ", " + str(p[3])
        p[0] = Node(p[2], [p[1], p[3]])

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = Node("neg", [p[2]])

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = Node("paren", [p[2]])

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = Node("int", [p[1]])

    def p_expression_decimal(self, p):
        'expression : DECIMAL'
        p[0] = Node("decimal", [p[1]])

    def p_expression_var(self, p):
        'expression : VARNAME'
#        print "HANDLING " + p[1]
        v = self.find_var(p[1])
        p[0] = Node("var", [v])

    def p_expression_frac(self, p):
        'expression : FRACSYMBOL LBRACE expression RBRACE LBRACE expression RBRACE'
        p[0] = Node("frac", [p[3], p[6]])

    def p_expression_result(self, p):
        'expression : RESULTSYMBOL LBRACE expression RBRACE'
        p[0] = Node("result", [p[3]])

    def p_expression_sqrt(self, p):
        'expression : SQRTSYMBOL LBRACE expression RBRACE LBRACE expression RBRACE'
        p[0] = Node("sqrt", [p[3], p[6]])

    def p_expression_stdform(self, p):
        'expression : STDFORMSYMBOL LBRACE expression RBRACE'
        p[0] = Node("stdform", [p[3]])

    def p_expression_decform(self, p):
        'expression : DECFORMSYMBOL LBRACE expression RBRACE'
        p[0] = Node("decform", [p[3]])

    def p_error(self, p):
        if p:
            sys.stderr.write("Syntax error at '%s'\n" % p.value)
            raise MyException("Syntax error at '%s'" % p.value)
        else:
            sys.stderr.write("Syntax error at EOF\n")
            raise MyException("Syntax error at EOF")

if __name__ == '__main__':
    calc = Calc()
    calc.run()
