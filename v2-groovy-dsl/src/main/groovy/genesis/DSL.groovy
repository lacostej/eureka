package genesis

import static genesis.MathUtils.*

class DSL {
  static def random = new Random()

  static NodeResultEvaluator nodeResultEvaluator = new NodeResultEvaluator();
  static NodeLatexConvertor nodeLatexConvertor = new NodeLatexConvertor();
  static NodeXmlConvertor nodeXmlConvertor = new NodeXmlConvertor();
  static NodeFormulaSimpleOuptutGenerator nodeFormulaSimpleOuptutGenerator = new NodeFormulaSimpleOuptutGenerator();


  static random(list) {
    return list[random.nextInt(list.size())]
  }

  static int r(range) {
    return random(range)
  }

  static add(a,b) {
    return new ENode('+', [a, b])
  }

  static sub(a,b) {
    return new ENode('-', [a, b])
  }
  /*
  static sign1(a, b) {
    return random([DSL.&add, DSL.&sub])(a,b)
  }
  */

  static sign1() {
    return random([DSL.&add, DSL.&sub])
  }

  static solve(ENode expression) {
    return new ENode("result", [expression])
  }
}

/** a simple tree implementation **/
class ENode {
  def type
  def children = []

  ENode(type, List children) {
    if (!(children instanceof List)) {
      throw new IllegalArgumentException("The ENode children parameter should be a List but is " + children.getClass() + " type: " + type)
    }
    this.type = type
    this.children = children
  }

  String toString() {
    return "ENode " + type  + ",("+ children.join(',') + ")"
  }
}

class MyException extends RuntimeException {
  MyException(s) { super(s) } 
}

/* A visitor that converts a tree to its XML reprensentation, usefull for debugging the conversion from formulat to Tree */
class NodeXmlConvertor {
  /* convert the node to an XML representation */
  def visit(node) {
    if (node == null)
      throw new MyException("node is None !!!")
    return this.nodeToXml(node)
  }

  /* recursive XML representation of the node */
  def nodeToXml(node) {
    if (node instanceof String) {
      return node
    }
    if (isNumber(node)) {
      return "<" + instanceClassName(node) + ">" + node + "</" + instanceClassName(node) + ">"
    }

    def ch = ""
    for (c in node.children) {
      if (c instanceof ENode) {
//        print "____ instance " + str(type(c))
        if (ch.size() > 0)
          ch += ","
        ch += this.nodeToXml(c)
      } else {
//        print "____ type " + str(type(c))
        if (ch.size() > 0)
          ch += ","
        ch += c
       }
    }
    def leafstr = ""
    //if (node.leaf)
    //  leafstr = "<leaf>" + this.nodeToXml(node.leaf) + "</leaf>"
    def result = "<node><type>" + node.type +  "</type><children>" + ch + "</children>" + leafstr + "</node>"
//    print result
    return result
  }

  /* Returns a String representation of a instance's class name */
  def instanceClassName(x) {
    // return type(x).__module__ + "." + type(x).__name__
    return x == null ? "null" : x.getClass().getName()
  }
}

/** A visitor that go through the tree and computes the values of the sub-tree wrapped inside a 'result' node */
class NodeResultEvaluator {
  def rec_count = 0 // note: not multi-thread friendly

  /* convert result expressions into their values whenever possible */
  def visit(node) {
//    print "EVALUATING " + toXmlConvertor.visit(node)
    def r = this.evaluateResult(node)
    // println "EVALUATED " + DSL.nodeXmlConvertor.visit(r)
    return r
  }

  def evaluateResult(node, evaluate=false) {
    this.rec_count += 1
    if (! (node instanceof ENode)) {
      this.rec_count -= 1
      return node
    }
    if (node.type == "result") {
      def r = this.evaluateResult(node.children[0], true)
      this.rec_count -= 1
      return r
    }
    def n = this.evaluate(node, evaluate)
    if (n != null) {
      this.rec_count -= 1
      return n
    }

    def newtype = node.type
    def children = []
    //def newleaf = null

    for (child in node.children)
      children << this.evaluateResult(child, evaluate)
      
    //if (node.leaf)
    //  newleaf = this.evaluateResult(node.leaf, evaluate)
    node = new ENode(newtype, children/*, newleaf*/)
    def n2 = this.evaluate(node, evaluate)
    if (n2 != null)
      node = n2
    this.rec_count -= 1
    return node
  }
// def power(i, j):

  def evaluate(node, evaluate) {
// print (' '*this.rec_count) + "EVALUATING " + evaluate + " " + DSL.nodeXmlConvertor.visit(node)
    def r = this.theevaluate(node, evaluate)
// if (r):
// print (' '*this.rec_count) + "EVALUATED " + str(evaluate) + " " + toXmlConvertor.visit(r)
    return r
  }

  def theevaluate(node, evaluate) {
// print "EVALUATING " + str(evaluate) + " " + toXmlConvertor.visit(node) + " " + node.type + " " + str(type(node.children[0])) + " "
// print type(node.children)
// print type(node.children[0])

//  vars are always evaluated
    if (isNumber(node)) {
      return node
    }
    if ((node.type == 'int' || node.type == 'decimal') && isNumber(node.children[0])) {
      // print "EVALUATING var " + str(node.children)
      return node.children[0]
    }
    if (node.type == 'var' && isNumber(node.children[0])) {
      // print "EVALUATING var " + str(node.children)
      return node.children[0]
    }

    if (node.type == 'stdform' && isNumber(node.children[0])) {
      return node
    }

    if (node.type == 'decform' && isNumber(node.children[0])) {
      return node
    }
    if (node.type == 'list') {
      l = []
      node.children.each { l << this.evaluateResult(it, evaluate) }
      return new ENode("list", l)
    }

    if (evaluate) {
      if (node.type == 'equals')
        return new ENode("equals", [this.evaluate(top, evaluate), this.evaluate(bottom, evaluate)])
      if (node.type == 'frac' && isInt(node.children[0]) && isInt(node.children[1]))
        return reduceToFracOrIntNode(node.children[0], node.children[1])
      if (node.type == "neg" && isNumber(node.children[0]))
        return -1 * node.children[0]
      if (node.type == 'frac' && isNumber(node.children[0]) && isNumber(node.children[1]))
        return decimal(node.children[0]) / decimal(node.children[1])
      if (node.type == 'paren' && isNumber(node.children[0]))
        return node.children[0]
      if (node.type in ['*', ':'] && isparen(node.children[0]))
        return this.evaluate(new ENode(node.type, [node.children[0].children[0], node.children[1]]), evaluate)
      if (node.type in ['*', ':'] && isparen(node.children[1]))
        return this.evaluate(new ENode(node.type, [node.children[0], node.children[1].children[0]]), evaluate)
      if (node.type == '^' && isInt(node.children[1])) {
        if (node.children[1] == 0)
          return 1
        if (node.children[1] == 1)
          return this.evaluate(node.children[0], evaluate)
      }
      if (node.type == '^' && isNumber(node.children[0]) && isNumber(node.children[1]))
        Math.pow(decimal(node.children[0]), decimal(node.children[1]))
      if (node.type == '-' && isNumber(node.children[0]) && isNumber(node.children[1]))
        return node.children[0] - node.children[1]
      if (node.type == '+' && isNumber(node.children[0]) && isNumber(node.children[1]))
        return node.children[0] + node.children[1]
      if (node.type == '*' && isNumber(node.children[0]) && isNumber(node.children[1]))
        return node.children[0] * node.children[1]
      if (node.type == ':' && isNumber(node.children[0]) && isNumber(node.children[1]))
        return decimal(node.children[0]) / node.children[1]
      if ((node.type == '+' || node.type == '-') && isIntOrFracInt(node.children[0]) && isIntOrFracInt(node.children[1])) {
        def sign = 1
        if (node.type == '-')
          sign = -1
        def top = topIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1]) + sign * topIntOrFracInt(node.children[1]) * bottomIntOrFracInt(node.children[0])
        def bottom = bottomIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        return reduceToFracOrIntNode(top, bottom)
      }
      if ((node.type == '*') && isIntOrFracInt(node.children[0]) && isIntOrFracInt(node.children[1])) {
        def top = topIntOrFracInt(node.children[0]) * topIntOrFracInt(node.children[1])
        def bottom = bottomIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        return reduceToFracOrIntNode(top, bottom)
      }
      if ((node.type == ':') && isIntOrFracInt(node.children[0]) && isIntOrFracInt(node.children[1])) {
        def top = topIntOrFracInt(node.children[0]) * bottomIntOrFracInt(node.children[1])
        def bottom = bottomIntOrFracInt(node.children[0]) * topIntOrFracInt(node.children[1])
        return reduceToFracOrIntNode(top, bottom)
      }
// return node
    }
  }
}


/* A tree visitor that converts the formula to String. Simplified. */
class NodeFormulaSimpleOuptutGenerator {

  def binaryOperators = [ '+', '-', ':', '*']

  /* conver result expressions into a String we can read */
  def visit(node) {
    def result = this.toString(node)
// print "RESULT " + str(result)
    return result
  }

  def toString(node) {
// print "toString: " + toXmlConvertor.visit(node)
    if (node == null)
      throw new MyException("node is null !")
    if (isNumber(node))
      return formatNumber(node)
    if (node instanceof String)
      return node
    if (node.type == 'list') {
      //l = []
      //node.children.each { l << this.toString(it) }
      return "(" + node.children.join(',') + ")"
    }
    if (node.type == "int")
      return this.toString(node.children[0])
    if (node.type == "decimal")
      return this.toString(node.children[0])
    if (node.type == "var") {
      def result = this.toString(node.children[0])
      if (node.children.size() > 1)
        result += "=" + this.toString(node.children[1])
      return result
    }
    if (node.type == "sqrt")
      return "sqrt(" + this.toString(node.children[0]) + "," + this.toString(node.children[1]) + ")"
    if (node.type == "eller")
      return this.toString(node.children[0]) + " eller " + str(this.toString(node.children[1]))
    if (node.type == "stdform") {
      if (isNumber(node.children[0]))
        return stdform(node.children[0])
      throw new MyException("The following node cannot be converted through stdform. Evaluation error ? Node: " + this.toString(node.children[0]))
    }
    if (node.type == "decform") {
      if (isNumber(node.children[0]))
        return decform(node.children[0])
      throw new MyException("The following node cannot be converted through decform. Evaluation error ? Node: " + this.toString(node.children[0]))
    }
    if (node.type == "neg")
      return "-" + this.toString(node.children[0])
    if (node.type == "equals")
      return this.toString(node.children[0]) + " = " + this.toString(node.children[1])
    if (node.type in this.binaryOperators)
      return this.toString(node.children[0]) + " " + node.type + " " + this.toString(node.children[1])
    if (node.type == "paren")
      return "(" + this.toString(node.children[0]) + ")"
    if (node.type == "frac")
      return this.toString(node.children[0]) + "/" + this.toString(node.children[1])
    if (node.type == "^")
      return this.toString(node.children[0]) + "^" + this.toString(node.children[1])

    if (node.type == "text")
      return node.children[0]

// if (node.type == "paren"):
// return "(" + this.toString(node.children[0]) + ")"
    if (! node instanceof String)
      throw new MyException("Node isn't yet converted to String: " + node)
    return node
  }
}

/* A tree visitor that converts the formula to its LaTex representation. */
class NodeLatexConvertor {
  def binaryOperators = [ '+', '-', ':', '*']

  def latexBinaryOperators = [
    '+': " + ",
    '-': " - ",
    ':': " \\div ",
    '*': " \\cdot "
  ]

  /* 'conver result expressions into a String that LaTeX can understand' */
  def visit(node) {
    def result = this.toString(node)
// print "RESULT " + str(result)
    return result
  }

  def toString(node) {
    if (node == null)
      throw new MyException("Node is null !")

// print "DEBUG: toString: " + toXmlConvertor.visit(node)

    if (isNumber(node))
      return formatNumber(node)
    if (node instanceof String)
      return node
    if (node.type == 'list') {
      // l = [this.toString(elem) for elem in node.children]
      return "(" + node.children.join(",") + ")"
    }
    if (node.type == "int")
      return this.toString(node.children[0])
    if (node.type == "decimal")
      return this.toString(node.children[0])
    if (node.type == "var") {
      def result = this.toString(node.children[0])
      if (node.children.size() > 1)
        result += "=" + this.toString(node.children[1])
      return result
    }
    if (node.type == "sqrt")
      return "\\sqrt[" + this.toString(node.children[0]) + "]{" + this.toString(node.children[1]) + "}"
    if (node.type == "eller")
      return this.visit(node.children[0]) + " eller " + this.visit(node.children[1])
    if (node.type == "stdform")
      return stdformLatex(node.children[0])
    if (node.type == "decform")
      return this.toString(decform(node.children[0]))
    if (node.type == "neg")
      return "-" + this.toString(node.children[0])
    if (node.type == "equals")
      return this.visit(node.children[0]) + " = " + this.visit(node.children[1])
    if (node.type in this.binaryOperators)
// print "HI HI"
      return this.toString(node.children[0]) + this.latexBinaryOperators[node.type] + this.toString(node.children[1])
    if (node.type == "paren")
      return "\\left(" + this.toString(node.children[0]) + "\\right)"
    if (node.type == "frac")
      return "\\frac{" + this.toString(node.children[0]) + "}{" + this.toString(node.children[1]) + "}"
    if (node.type == "^")
      return this.toString(node.children[0]) + "^{" + this.toString(node.children[1]) + "}"

    if (node.type == "text")
// print "text: " + node.children
      return node.children[0]

// if (node.type == "paren"):
// return "(" + this.toString(node.children[0]) + ")"
    if (! node instanceof String)
      throw new MyException("Node isn't yet converted to String: " + node)
    return node
  }
}
