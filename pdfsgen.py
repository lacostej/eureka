import sys
import excelparse
import mathparse

import time
import os

def generateOuputLatexFileName(student, date):
  return student.shortName + ".latex"

if __name__ == "__main__":
  interfaceFile = sys.argv[1]
  exercisesFile = sys.argv[2]

  print "Parsing %s" % interfaceFile
  classStatus = excelparse.parse(interfaceFile)
  print str(len(classStatus.students)) + " student(s)"

  f = open(exercisesFile)
  exercisesData = f.read()
  exercises = mathparse.parseFile(exercisesData)

  os.chdir('gen')

  for student in classStatus.students:
    print "Handling student : " + student.fullName
    data = classStatus.getStudentData(student.shortName)
    if (not data):
      print "WARNING: missing data for student: " + str(student)
      continue
    if (not data.shouldGenerate):
      print "INFO: student will not have data generated: " + str(student)
      continue
    outputFileName = generateOuputLatexFileName(student, time.time())
    mathparse.generateLatexExercisesForStudent(exercises, "gen", outputFileName, student, data)
    print "Generated " + outputFileName
    os.system('latex -interaction nonstopmode ' + outputFileName)
#  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)"
