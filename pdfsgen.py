import sys
import excelparse
import mathparse

if __name__ == "__main__":
  filename = sys.argv[1]
  print "Parsing %s" & filename
  classStatus = excelparse.parse()
  print str(len(classStatus.students)) + " student(s)"
  print str(len(classStatus.exercises)) + " exercise(s)" 
