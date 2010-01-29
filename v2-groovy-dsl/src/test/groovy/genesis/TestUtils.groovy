package genesis

/**
 * Created by IntelliJ IDEA.
 * @author jerome@coffeebreaks.org
 * @since  Jan 27, 2010 9:59:37 PM
 */
class TestUtils {


  static def getResult(node) {
    return DSL.nodeResultEvaluator.visit(node)
  }

  static def resourceAsText(resourceName) {
    InputStream stream = resourceAsStream(resourceName)
    if (stream == null) {
      throw new NullPointerException("Resource " + resourceName + " not found");
    }
    return stream.getText()
  }

  static def resourceAsStream(resourceName) {
    def stream = Thread.currentThread().getContextClassLoader().getResourceAsStream(resourceName)
    if(stream == null){
      stream = getClass().getResourceAsStream(resourceName)
    }
    if(stream == null && System.getClassLoader() != null){
      stream = System.getClassLoader().getResourceAsStream(resourceName)
    }
    return stream
  }
}
