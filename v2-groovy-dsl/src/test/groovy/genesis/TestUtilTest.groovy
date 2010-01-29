package genesis

import static genesis.TestUtils.*

class TestUtilTest extends GroovyTestCase {

  void testSplitFile() {
    def s = resourceAsText("genesis/exercise_bag1.txt")

    def list = TextUtil.split(s, "^---.*");

    assertNotNull list
    assertEquals 3, list.size()

    assertEquals "a = 0\n", list[0]
    assertEquals "b = 1\n", list[1]
    assertEquals "// c = 2\n", list[2]
  }


}