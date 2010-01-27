package genesis

import static genesis.TestUtils.*

class ExerciseTest extends GroovyTestCase {

  void testReadOneExercise() {
    def exo = Exercise.fromText(resourceAsText("genesis/exercise1.txt"))

    assertNotNull exo: "could read the exercise"
    assert exo.getVariable('id') == 0
    assert exo.getVariable('a') >= 1 && exo.getVariable('a') <= 10
    assert Math.abs((int)exo.getVariable('b')) == 1
  }

  void testPefReadingOneExercise() {
    def text = resourceAsText("genesis/exercise1.txt")
    long start = System.currentTimeMillis()
    def n = 50
    n.times {
      Exercise.fromText(text)
    }
    println n + " exercices took: " + ((System.currentTimeMillis() - start) / n) + " ms" 
  }
}
