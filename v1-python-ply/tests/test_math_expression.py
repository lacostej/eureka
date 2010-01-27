import math_expression
from assert_utils import *
from decimal import *

def test___decstr__():
  s = "0.00000000000001"
  assertEquals(s, math_expression.__decstr(Decimal(s)))


