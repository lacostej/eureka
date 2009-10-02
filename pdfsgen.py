import sys
import excelparse
import mathparse

import time
import os

import mailer

def fileBaseName(student):
  return student.shortName.replace(" ", "_")

def main(interfaceFile, exercisesFile, sendMails=False):
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
    print "Handling student : " + student.fullName.encode("iso-8859-1")
    data = classStatus.getStudentData(student.shortName)
    if (not data):
      print "WARNING: missing data for student: " + str(student)
      continue
    if (not data.shouldGenerate):
      print "INFO: student will not have data generated: " + str(student)
      continue

    outputFileName = fileBaseName(student) + ".latex"
    resultOutputFileName = fileBaseName(student) + "_result.latex"

    mathparse.generateLatexExercisesAndResultsForStudent(exercises, classStatus.sortedExoIDs, "gen", outputFileName, resultOutputFileName, student, data)
    print "Generated " + outputFileName + " and " + resultOutputFileName

    if (not os.access(outputFileName, os.F_OK)):
      print "ERROR: couldn't find the Exercise Latex file. Check the logs"
      continue
    if (not os.access(resultOutputFileName, os.F_OK)):
      print "ERROR: couldn't find the Results Latex file. Check the logs"
      continue

    os.system('latex -interaction nonstopmode ' + outputFileName + " 2>&1 >> full_gen.log")
    os.system('latex -interaction nonstopmode ' + resultOutputFileName + " 2>&1 >> full_gen.log")

    userPdfDir = "pdfs/" + fileBaseName(student)

    userExosPdfFile = fileBaseName(student) + ".pdf"
    userResultsPdfFile = fileBaseName(student) + "_result.pdf"
    if (not os.access(userExosPdfFile, os.F_OK)):
      print "ERROR: couldn't generate the Exercise PDF. Check the logs"
      continue
    if (not os.access(userResultsPdfFile, os.F_OK)):
      print "ERROR: couldn't generate the Result PDF. Check the logs"
      continue
    if (not os.access("pdfs", os.F_OK)):
      os.mkdir("pdfs")
    if (not os.access(userPdfDir, os.F_OK)):
      os.mkdir(userPdfDir)
    os.rename(userExosPdfFile, userPdfDir + "/" + userExosPdfFile)
    os.rename(userResultsPdfFile, userPdfDir + "/" + userResultsPdfFile)

    if (sendMails and student.shortName == "jerome"):
      f = (userPdfDir + "/" + userExosPdfFile).encode("iso-8859-1")
      open(f, "rb").read()
      print f
      mailer.send_mail("eureka@vgsn.no", [student.email], "Latest exercises from vgsn", "Bla bla bla", [f], "smtp.gmail.com", "jbhkp.eureka", "jVsmpdg1*")

#  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)"
if __name__ == "__main__":
  interfaceFile = sys.argv[1]
  exercisesFile = sys.argv[2]

  main(interfaceFile, exercisesFile)
