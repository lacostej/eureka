from utils import *
import xlrd

class ClassStatus:

  def __init__(self, students, sortedExoIDs, studentExercicesStatus):
    self.students = students
    self.sortedExoIDs = sortedExoIDs
    self.studentExercicesStatus = studentExercicesStatus

  def getStudentData(self, shortName):
    return find(self.studentExercicesStatus, lambda ses : ses.studentId == shortName)
    
class Student:
  def __init__(self, shortName, fullName, email):
    self.shortName = shortName
    self.fullName = fullName
    self.email = email

  def __str__(self):
    return self.shortName + " (\"" + str(self.fullName) + "\" <" + str(self.email) + ">)"

class StudentExercicesStatus:
  def __init__(self, studentId, uComment, shouldGenerate, exerciseStatuses):
    self.studentId = studentId
    self.uComment = uComment
    self.shouldGenerate = shouldGenerate
    self.exerciseStatuses = exerciseStatuses

class ExerciseStatus:
  def __init__(self, exerciseId, status, toGenerate):
    self.exerciseId = exerciseId
    self.status = status
    self.toGenerate = toGenerate

  def __str__(self):
    return self.exerciseId + ":" + str(self.status) + "," + str(self.toGenerate)

def parse(fileName):
  book = xlrd.open_workbook(fileName)
#  print "worksheets", book.nsheets
  if (book.nsheets < 2):
    raise MyException("Number of sheets is invalid. We expect at least 2 sheets.")

  students = []
  studentSheet = book.sheet_by_index(0)
#  print studentSheet.name, studentSheet.nrows, studentSheet.ncols
  if (studentSheet.ncols < 3): 
    raise MyException("Number of columns in sheet 1 '%s' is invalid. We expect 3 columns." & studentSheet.ncols)
  for rx in range(studentSheet.nrows):
    if (rx == 0):
      continue # skip header
    row = studentSheet.row(rx)
    students.append(Student(row[0].value.strip().encode("utf-8"), row[1].value.strip().encode("utf-8"), row[2].value.strip()))

  studentsExercisesStatus = []
  exercisesSheet = book.sheet_by_index(1)
#  print exercisesSheet.name, exercisesSheet.nrows, exercisesSheet.ncols
#  if (studentSheet.ncols < 3): 
#    raise MyException("Number of columns in sheet 1 '%s' is invalid. We expect 3 columns." & studentSheet.ncols)

  startStudentColumnIdx = 4
  startExerciseRowId = 3

  sortedExoIDs = []
  firstStudent = True

  for cx in range(startStudentColumnIdx, exercisesSheet.ncols, 2):
    shouldGenerate = False
    uComment = None

    exerciseStatuses = {}
    uStudentId = exercisesSheet.cell(2, cx).value
    studentId = uStudentId.encode("utf-8")
#    print "Treating student: " + studentId

    uStudentId2 = exercisesSheet.cell(2, cx+1).value
    studentId2 = uStudentId.encode("utf-8")
    if (studentId != studentId2):
#      print cx 
      raise MyException("The 2 columns for student don't have matching names " + studentId + " and " + studentId2)


    commentCell = exercisesSheet.cell(0, cx+1)
    if commentCell.ctype != xlrd.XL_CELL_EMPTY:
      if commentCell.ctype == xlrd.XL_CELL_TEXT:
        uComment = commentCell.value

    genCell = exercisesSheet.cell(1, cx+1)
    if genCell.ctype == xlrd.XL_CELL_NUMBER:
#      print genCell.ctype
      if genCell.value == 1.0:
        shouldGenerate = True

    for rx in range(startExerciseRowId, exercisesSheet.nrows):
      exoStatus = 0
      exoToGen = 0
      uExoId = exercisesSheet.cell(rx, 1).value
      exoId = uExoId.encode("utf-8")
      if (firstStudent):
        sortedExoIDs.append(exoId)
      if exercisesSheet.cell(rx, cx+1).ctype == xlrd.XL_CELL_NUMBER:
        exoStatus =  int(exercisesSheet.cell(rx, cx+1).value)
      if exercisesSheet.cell(rx, cx).ctype == xlrd.XL_CELL_NUMBER:
        exoToGen =  int(exercisesSheet.cell(rx, cx).value)
#       print exoId, exoStatus, exoToGen
      exerciseStatus = ExerciseStatus(exoId, exoStatus, exoToGen)
      exerciseStatuses[exoId] = exerciseStatus
    studentsExercisesStatus.append(StudentExercicesStatus(studentId, uComment, shouldGenerate, exerciseStatuses))
    firstStudent = False
  return ClassStatus(students, sortedExoIDs, studentsExercisesStatus)


if __name__ == "__main__":
  classStatus = parse(sys.argv[1])
  print str(len(classStatus.studentExercicesStatus)) + " student(s) exercices status"

