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

class FormulaParser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
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
      return self.parser.parse(s, lexer=self.formulaLexer)

class Node:
  def __init__(self,type,children=None,leaf=None):
    self.type = type
    if children:
      self.children = children
    else:
      self.children = [ ]
    self.leaf = leaf

class NodeXmlConvertor:
#  def __init__(self):
#    pass

  def visit(self, node):
    'convert the node to an XML representation'
    return self.nodeToXml(node)

  def nodeToXml(self, node):
    'recursive XML representation of the node'
    ch = ""
#    print self.children
    for c in node.children:
      if (isinstance(c, Node)):
#        print "____ instance " + str(type(c))
        if len(ch) > 0:
          ch += ","
        ch += self.nodeToXml(c)
      else:
#        print "____ type " + str(type(c))
        if len(ch) > 0:
          ch += ","
        ch += str(c)
    leafstr = ""
    if node.leaf:
      leafstr = "<leaf>" + self.nodeToXml(node.leaf) + "</leaf>"
    return "<node><type>" + str(node.type) +  "</type><children>" + ch + "</children>" + leafstr + "</node>"

class Calc(FormulaParser):

    tokens = (
        'NUMBER',
        'PLUS','MINUS','POWER','TIMES','DIVIDE','EQUALS', #,'EXP'
        'LPAREN','RPAREN',
        'LBRACE','RBRACE',
        'VARNAME', 'RESULTSYMBOL', 'FRACSYMBOL', 'SQRTSYMBOL', 'STDFORMSYMBOL'
        )

    # Tokens

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
#    t_EXP     = r'\*\*'
    t_TIMES   = r'\*'
    t_POWER   = r'\^'
    t_DIVIDE  = r':'
    t_EQUALS  = r'='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
    t_VARNAME = r'[a-z]'
    t_RESULTSYMBOL = r'\\res'
    t_FRACSYMBOL = r'\\frac'
    t_SQRTSYMBOL = r'\\sqrt'
    t_STDFORMSYMBOL = r'\\stdform'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        #print "parsed number %s" % repr(t.value)
        return t

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
        print("Undefined name '%s'" % x)
        raise e

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression VARNAME expression
        """
        #print [repr(p[i]) for i in range(0,4)]
        ops = [ '+', '-', '*', ':', '^']
        if not p[2] in ops:
          p[2] = self.find_var(p[2])

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

    def p_expression_var(self, p):
        'expression : VARNAME'
#        print "HANDLING " + p[1]
        try:
            v = self.names[p[1]]
            p[0] = Node("var", [v])
#            if (isinstance(v) == int):
#              p[0] = Node("int", v)
#            else:
#              p[0] = Node("var", v)

        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_expression_frac(self, p):
        'expression : FRACSYMBOL LBRACE expression RBRACE LBRACE expression RBRACE'
        p[0] = Node("frac", [p[3], p[6]])

    def p_expression_result(self, p):
        'expression : RESULTSYMBOL LBRACE expression RBRACE'
        p[0] = Node("result", [p[3]])

    def p_expression_sqrt(self, p):
        'expression : SQRTSYMBOL LBRACE expression RBRACE LBRACE expression RBRACE'
        p[0] = Node("sqrt", [p[3], p[6]])

    def p_expression_equals(self, p):
        'expression : expression EQUALS expression'
        p[0] = Node("equals", [p[1], p[3]])

    def p_expression_stdform(self, p):
        'expression : STDFORMSYMBOL LBRACE expression RBRACE'
        p[0] = Node("stdform", [p[2]])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    calc = Calc()
    calc.run()
