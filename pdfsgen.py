import sys
import excelparse
import mathparse

import time
import os

def fileBaseName(student):
  return student.shortName.replace(" ", "_")

def generateOuputLatexFileName(student, date):
  return fileBaseName(student) + ".latex"

if __name__ == "__main__":
  interfaceFile = sys.argv[1]
  exercisesFile = sys.argv[2]

  print "Parsing %s" % interfaceFile
  classStatus = excelparse.parse(interfaceFile)
  print str(len(classStatus.students)) + " student(s)"

  f = open(exercisesFile)
  exercisesData = f.read()
  exercises = mathparse.parseFile(exercisesData)

  if (not os.access("gen", os.F_OK)):
    os.mkdir("gen")

  os.chdir('gen')

  os.system('rm full_gen.log')
  os.system('touch full_gen.log')

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

    if (not os.access(outputFileName, os.F_OK)):
      print "ERROR: couldn't find the Latex file. Check the logs"
      continue

    os.system('latex -interaction nonstopmode ' + outputFileName + " 2>&1 >> full_gen.log")

    userPdfDir = "pdfs/" + fileBaseName(student)

    userPdfFile = fileBaseName(student) + ".pdf"
    if (not os.access(userPdfFile, os.F_OK)):
      print "ERROR: couldn't generate the PDF. Check the logs"
      continue
    if (not os.access("pdfs", os.F_OK)):
      os.mkdir("pdfs")
    if (not os.access(userPdfDir, os.F_OK)):
      os.mkdir(userPdfDir)
    os.rename(userPdfFile, userPdfDir + "/" + userPdfFile)
#  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)"
