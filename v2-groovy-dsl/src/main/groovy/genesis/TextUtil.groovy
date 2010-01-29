package genesis

/**
 * Created by IntelliJ IDEA.
 * @author jerome@coffeebreaks.org
 * @since  Jan 29, 2010 10:00:29 AM
 */
class TextUtil {

  static def split(String text, pattern) {
    def res = []
    StringBuilder builder = new StringBuilder()
    text.readLines().each {
      if (it ==~ pattern) {
        if (builder.toString() != "") {
          res << builder.toString()
          builder = new StringBuilder()
        }
      } else {
        builder << it + "\n"
      }
    }
    return res
  }
}
