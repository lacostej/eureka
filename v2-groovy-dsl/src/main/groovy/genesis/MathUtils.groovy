package genesis

import java.text.DecimalFormat

/**
 * Created by IntelliJ IDEA.
 * @author jerome@coffeebreaks.org
 * @since  Jan 28, 2010 6:45:12 AM
 */

static def decimal(d) {
    return new Double(d)
}

static def isparen(node) {
  return node instanceof Node && node.type == "paren"
}

/* Returns the standard form representation of a number as a string */
static def stdform(d) {
  if (d instanceof int) {
    d = decimal(d)
  }
  throw new IllegalStateException("Not re-implemented")
/*  if (!d instanceof decimal("0").class) {
    print "ERROR :" + type(d) + " " + d
  }

// print str(10**(-d.adjusted()))
  s = str((d*decimal(str(10**(-d.adjusted())))).normalize().quantize(decimal("0.00")).normalize())
  if (d.adjusted() != 0):
// s += "E" + str(d.adjusted())
    s += " * 10^" + str(d.adjusted())
  return s
  */
  }

/* Returns the full representation of a number as a string */
static def decform(d) {
  return d.toString()
  /*
  if (isInt(d)) {
    return d.toString()
  }
// print "DECFORM " + str(type(d)) + " " + __decstr(d)
  return __decstr(d)
  */
}

/*
def __decstr(d):
  '''Return string representation of the decimal in scientific notation.
   Captures all of the information in the underlying representation.
   VARIATION FROM PYTHON2.6 decimal.Decimal.__str__ where scientitic notation doesn't exist
  '''

  sign = ['', '-'][d._sign]
  if d._is_special:
    if d._exp == 'F':
      return sign + 'Infinity'
    elif d._exp == 'n':
      return sign + 'NaN' + d._int
    else: # this._exp == 'N'
      return sign + 'sNaN' + d._int

//  number of digits of this._int to left of decimal point
  leftdigits = d._exp + len(d._int)

//  dotplace is number of digits of this._int to the left of the
//  decimal point in the mantissa of the output string (that is,
//  after adjusting the exponent)
  if d._exp <= 0 && leftdigits > -100:
//  no exponent required
    dotplace = leftdigits
  elif not eng:
//  usual scientific notation: 1 digit on left of the point
    dotplace = 1
  elif d._int == '0':
//  engineering notation, zero
    dotplace = (leftdigits + 1) % 3 - 1
  else:
//  engineering notation, nonzero
    dotplace = (leftdigits - 1) % 3 + 1

  if dotplace <= 0:
    intpart = '0'
    fracpart = '.' + '0'*(-dotplace) + d._int
  elif dotplace >= len(d._int):
    intpart = d._int+'0'*(dotplace-len(d._int))
    fracpart = ''
  else:
    intpart = d._int[:dotplace]
    fracpart = '.' + d._int[dotplace:]
  if leftdigits == dotplace:
    exp = ''
  else:
    if context is null:
      context = getcontext()
      exp = ['e', 'E'][context.capitals] + "%+d" % (leftdigits-dotplace)

  return sign + intpart + fracpart + exp
*/

/* Returns the standard form representation of a number as a string */
static def stdformLatex(d) {
  if (d instanceof int)
    d = decimal(d)
  if (! isDecimal(d))
    print "ERROR :" + str(type(d)) + " " + str(d)
// print str(10**(-d.adjusted()))
  /*
  def s = str((d*decimal(str(10**(-d.adjusted())))).normalize().quantize(decimal("0.00")).normalize())
  if (d.adjusted() != 0):
    s += " \cdot 10^{" + str(d.adjusted()) + "}"
  return s
  */
  throw new IllegalStateException("Not re-implemented")
}
/* Returns the top of a fraction of integers or the integer value. Used to compute fracOrInt operations */
static def topIntOrFracInt(intOrFrac) {
  if (! isIntOrFracInt(intOrFrac))
    throw new MyException(intOrFrac + " of type " + intOrFrac.getClass())
// print toXmlConvertor.visit(intOrFrac)
  if (isInt(intOrFrac))
    return intOrFrac
  return intOrFrac.children[0]
}
/* Returns the bottom of a fraction of integers or the integer value. Used to compute fracOrInt operations */
static def bottomIntOrFracInt(intOrFrac) {
  if (! isIntOrFracInt(intOrFrac))
    throw new MyException(str(intOrFrac) + " of type " + intOrFrac.getClass())
// print toXmlConvertor.visit(intOrFrac)
  if (isInt(intOrFrac))
    return 1
  return intOrFrac.children[1]
}

static def reduceToFracOrIntNode(top, bottom) {
  // FIXME (top, bottom) = reduceFrac(top, bottom)
  def a = reduceFrac(top, bottom)
  top = a[0]
  bottom = a[1]
  
  if (bottom == 1) {
    return top
  }
  def negative = top < 0
  def n = new ENode("frac", [abs(top), bottom])
  if (negative)
    n = new ENode("neg", [n])
  return n
}

/* Reduces a fraction of integers. E.g. 30,35 -> 6,7. Returns a new couple of integers representing the fraction. top can be positive. */
static def reduceFrac(top, bottom) {
  if (bottom == 0) {
    return [top, bottom]
  }
  def sign = 1
  if (top * bottom < 0)
    sign = -1

  top = abs(top)
  bottom = abs(bottom)

  def a = split(top)
  def b = split(bottom)
  def x = 0
  while (x < a.size()) {
    def i = a[x]
    if (i in b) {
      a.remove(i)
      b.remove(i)
      top = top / i
      bottom = bottom / i
    }
    else {
      x += 1
    }
  }
  return [sign*top, bottom]
}

/* Returns True if the parameter is an int or fraction of integers. */
static def isIntOrFracInt(x) {
  return x instanceof int || (x instanceof Node && x.type == "frac" && x.children[0] instanceof int && x.children[1] instanceof int)
}
/* Returns True if the parameter is an int. */
static def isInt(x) {
  return x instanceof Integer
}

/* Returns True if the parameter is an decimal. */
static def isDecimal(x) {
  return x instanceof Double
}

/* Returns True if the parameter is an int or decimal. */
static def isNumber(x) {
  return isInt(x) || isDecimal(x)
}

static def remove_exponent(d) {
  throw new IllegalStateException("not re-implemented")
  // return d.quantize(decimal(1)) if d == d.to_integral() else d.normalize()
}

static def formatNumber(node) {
  if (isInt(node))
    return node.toString()
  DecimalFormat format = new DecimalFormat("#0.00");
  return format.format(node);
//  TWOPLACES = decimal('0.01')
//  return str(remove_exponent(node.quantize(TWOPLACES)))
}

