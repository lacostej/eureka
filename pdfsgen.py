import sys
import excelparse
import mathparse

if __name__ == "__main__":
  filename = sys.argv[1]
  print "Parsing %s" % filename
  classStatus = excelparse.parse(filename)
  print str(len(classStatus.students)) + " student(s)"
#  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)"
