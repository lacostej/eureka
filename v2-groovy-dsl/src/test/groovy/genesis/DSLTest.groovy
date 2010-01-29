package genesis

import static genesis.TestUtils.*

class DSLTest extends GroovyTestCase {

  void testResultEvaluatorSimpleAddOrSub() {
    assertEquals 0, getResult(DSL.solve(new ENode('-', [1, 1])))
    assertEquals 2, getResult(DSL.solve(new ENode('+', [1, 1])))
  }
}