import sys
import excelparse
import mathparse

import time
import datetime
import os

import mailer
from utils import *

def fileBaseName(student):
  return student.shortName.replace(" ", "_")

def main(interfaceFile, exercisesFile, pdflink, sendMails=False):
  print "Parsing %s" % interfaceFile
  classStatus = excelparse.parse(interfaceFile)
  print str(len(classStatus.students)) + " student(s)"

  f = open(exercisesFile)
  exercisesData = f.read()
  exercises = mathparse.parseFile(exercisesData)

  now = datetime.datetime.utcnow()

  if os.access("gen", os.F_OK):
    if os.path.islink("gen"):
      os.unlink("gen")
    else:
      raise MyException("gen exists but isn't a link")

  target = "gen_" + now.strftime("%Y%m%d-%H%M%S")
  if (not os.access(target, os.F_OK)):
    os.mkdir(target)
    os.symlink(os.path.abspath(target), "gen")

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

    userExosPdfFile = fileBaseName(student) + ".pdf"
    userResultsPdfFile = fileBaseName(student) + "_result.pdf"
    if (not os.access(userExosPdfFile, os.F_OK)):
      print "ERROR: couldn't generate the Exercise PDF. Check the logs"
      continue
    if (not os.access(userResultsPdfFile, os.F_OK)):
      print "ERROR: couldn't generate the Result PDF. Check the logs"
      continue

    if (not os.access("pdfs", os.F_OK)):
      if pdflink != None:
        os.symlink(os.path.abspath(pdflink), "pdfs")
      else:
        os.mkdir("pdfs")

    userPdfDir = "pdfs/" + fileBaseName(student)
    if (not os.access(userPdfDir, os.F_OK)):
      os.mkdir(userPdfDir)

    os.rename(userExosPdfFile, userPdfDir + "/" + userExosPdfFile)
    os.rename(userResultsPdfFile, userPdfDir + "/" + userResultsPdfFile)

    if (sendMails):
      f = (userPdfDir + "/" + userExosPdfFile)
      open(f, "rb").read()
#      print f
      now = datetime.datetime.utcnow()
      week = now.strftime("%W")
      comment = __u(data.comment)
      if (comment == None):
        comment = ""
      comment = comment + "\n"
      text = "Hei,\n" + comment + __u(ur"\u00d8velse gj\u00f8r mester") + "\nLykke til!\nJean"
      mailer.send_mail("eureka@vgsn.no", [student.email], "Matematikk lekser (uke " + week + ")", text, [f], "smtp.gmail.com", "jbhkb.eureka", "jVsmpdg1*")

  del exercises

#  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)"
if __name__ == "__main__":
  interfaceFile = sys.argv[1]
  exercisesFile = sys.argv[2]
  if (len(sys.argv) > 3):
    pdflink = sys.argv[3]
  else:
    pdflink = None

  main(interfaceFile, exercisesFile, pdflink, True)
