package genesis

class Exercise {
  Map variables

  public Exercise(java.util.Map vars) {
    variables = vars
  }

  def getVariable(name) {
    return variables[name]
  }

  static def fromText(String s) {
    Binding binding = new Binding();
    // binding.setVariable("foo", new Integer(2));
    GroovyShell shell = new GroovyShell(binding);
    def exo_header = """\
import static genesis.DSL.*
"""
    shell.evaluate(exo_header + s)
    
    return new Exercise(binding.getVariables())
  }

  static List<Exercise> multipleFromText(String s) {
    return TextUtil.split(s, "^---.*").collect{ Exercise.fromText(it)}
  }
}
