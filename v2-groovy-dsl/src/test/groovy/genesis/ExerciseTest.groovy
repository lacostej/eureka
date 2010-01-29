package genesis

import static genesis.TestUtils.*

class ExerciseTest extends GroovyTestCase {

  void testReadOneExercise() {
    def exo = Exercise.fromText(resourceAsText("genesis/exercise1.txt"))

    assertNotNull exo: "could read the exercise"
    assert exo.getVariable('desc') == "Compute this operation: "
    assert exo.getVariable('id') == 0
    assert exo.getVariable('a') >= 1 && exo.getVariable('a') <= 10
    assert Math.abs((int) exo.getVariable('b')) == 1
    assert exo.getVariable('exercise') instanceof ENode
    def solution = exo.getVariable('solution')
    println solution.toString() + " evaluates to: " + getResult(solution)
  }

  void testReadMultipleExercises() {
    List<Exercise> list = Exercise.multipleFromText(resourceAsText("genesis/exercise_bag1.txt"))

    assertEquals 3, list.size()

    assertEquals 1, list[0].variables.size()
    assertEquals 0, list[0].getVariable('a')

    assertEquals 1, list[1].variables.size()
    assertEquals 1, list[1].getVariable('b')

    assertEquals 0, list[2].variables.size()
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
