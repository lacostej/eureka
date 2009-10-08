import sys
import excelparse
import mathparse

import time
import datetime
import os

import mailer
import pdfs
from utils import *
import htmlutils

def fileBaseName(student):
  return student.shortName.replace(" ", "_")

def main(interfaceFile, exercisesFile, pdflink):
  print "Parsing %s" % interfaceFile

  prof_name = os.path.splitext(os.path.basename(interfaceFile))[0]

  classStatus = excelparse.parse(interfaceFile)
  print str(len(classStatus.students)) + " student(s)"

  f = open(exercisesFile)
  exercisesData = f.read()
  exercises = mathparse.parseFile(exercisesData)

  now = datetime.datetime.utcnow()

  # temporary cleanup
  if os.access("gen", os.F_OK):
    if os.path.islink("gen"):
      os.unlink("gen")

  if os.access("latest", os.F_OK):
    if os.path.islink("latest"):
      os.unlink("latest")
    else:
      raise MyException("latest exists but isn't a link")

  gen = "gen"
  if os.path.islink(gen):
    os.unlink(gen)
  if (not os.access(gen, os.F_OK)):
    os.mkdir(gen)

  target = os.path.join(gen, prof_name + "_" + now.strftime("%Y%m%d-%H%M%S"))

  if (not os.access(target, os.F_OK)):
    os.mkdir(target)
    os.symlink(os.path.abspath(target), "latest")

  os.chdir('latest')

  os.system('rm full_gen.log')
  os.system('touch full_gen.log')

  now = datetime.datetime.utcnow()
  realYear, week, day = now.isocalendar()
  week = str(week)

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

    mathparse.generateLatexExercisesAndResultsForStudent(exercises, classStatus.sortedExoIDs, target, outputFileName, resultOutputFileName, student, data)
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

    teacher_pdf_dir = os.path.join("pdfs", prof_name)
    if (not os.access(teacher_pdf_dir, os.F_OK)):
      if pdflink != None:
        online_teacher_pdf_dir = os.path.join(os.path.abspath(pdflink), prof_name)
        if not os.path.exists(online_teacher_pdf_dir):
          os.mkdir(online_teacher_pdf_dir)
#        print online_teacher_pdf_dir
#        print teacher_pdf_dir
        os.symlink(pdflink, "pdfs")
      else:
        online_teacher_pdf_dir = teacher_pdf_dir
        os.mkdir(teacher_pdf_dir)

    studentPdfDir = os.path.join(teacher_pdf_dir, fileBaseName(student))
    if (not os.access(studentPdfDir, os.F_OK)):
      os.mkdir(studentPdfDir)

    exosPath = (studentPdfDir + "/" + userExosPdfFile)
    resultsPath = (studentPdfDir + "/" + userResultsPdfFile)

    os.rename(userExosPdfFile, exosPath)
    os.rename(userResultsPdfFile, resultsPath)

    if (classStatus.email):
#      open(f, "rb").read()
#      print f
      comment = u(data.uComment)
      if (comment == None):
        comment = ""
      comment = comment + "\n"
      text = "Hei,\n" + comment + u(ur"\u00d8velse gj\u00f8r mester") + "\nLykke til!\nJean"
      send_mail("eureka@vgsn.no", [student.email], "Matematikk lekser (uke " + week + ")", text, [exosPath])

      send_mail("eureka@vgsn.no", ["jeanbaptiste.huynh@gmail.com"], "Matematikk lekser (uke " + week + ") for " + student.fullName, text, [exosPath, resultsPath])

  htmlutils.gen_index("pdfs")
  htmlutils.gen_index(online_teacher_pdf_dir)

  pdfs.pdf_all_combine_to_file("exos_combined.latex", teacher_pdf_dir, "**.pdf", "**_result.pdf")
  pdfs.pdf_all_combine_to_file("results_combined.latex", teacher_pdf_dir, "**_result.pdf", None)
  send_mail("eureka@vgsn.no", ["jerome.lacoste@gmail.com"], "Matematikk lekser og resultater (uke " + week + ") for alle", "", ["exos_combined.pdf", "results_combined.pdf"])
#  send_mail("eureka@vgsn.no", ["jerome.lacoste@gmail.com"], "Matematikk lekser og resultater (uke " + week + ") for alle", "", ["exos_combined.pdf", "results_combined.pdf"])

  del exercises

def send_mail(fromEmail, toEmails, subject, content, files):
  mailer.send_mail(fromEmail, toEmails, subject, content, files, "smtp.gmail.com", "jbhkb.eureka", "jVsmpdg1*")

#  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)"
if __name__ == "__main__":
  interfaceFile = sys.argv[1]
  exercisesFile = sys.argv[2]
  if (len(sys.argv) > 3):
    pdflink = sys.argv[3]
  else:
    pdflink = None

  main(interfaceFile, exercisesFile, pdflink)
