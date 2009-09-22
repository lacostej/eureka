from utils import *
import xlrd

class ClassStatus:

  def __init__(self, students, studentExercicesStatus):
    self.students = students
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
  def __init__(self, studentId, comment, shouldGenerate, exerciseStatuses):
    self.studentId = studentId
    self.comment = comment
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
    students.append(Student(row[0].value.strip(), row[1].value.strip(), row[2].value.strip()))

  studentsExercisesStatus = []
  exercisesSheet = book.sheet_by_index(1)
#  print exercisesSheet.name, exercisesSheet.nrows, exercisesSheet.ncols
#  if (studentSheet.ncols < 3): 
#    raise MyException("Number of columns in sheet 1 '%s' is invalid. We expect 3 columns." & studentSheet.ncols)

  startStudentColumnIdx = 4
  startExerciseRowId = 3

  for cx in range(startStudentColumnIdx, exercisesSheet.ncols, 2):
    shouldGenerate = False
    comment = None

    exerciseStatuses = {}
    studentId = exercisesSheet.cell(2, cx).value
    studentId = studentId.encode("iso-8859-1")
#    print "Treating student: " + studentId

    commentCell = exercisesSheet.cell(0, cx+1)
    if commentCell.ctype != xlrd.XL_CELL_EMPTY:
      if commentCell.ctype == xlrd.XL_CELL_TEXT:
        comment = commentCell.value

    if (studentId != exercisesSheet.cell(2, cx+1).value):
#      print cx 
      raise MyException("The 2 columns for student don't have matching names " + studentId + " and " + exercisesSheet.cell(2, cx+1).value)

    genCell = exercisesSheet.cell(1, cx+1)
    if genCell.ctype == xlrd.XL_CELL_NUMBER:
#      print genCell.ctype
      if genCell.value == 1.0:
        shouldGenerate = True

    for rx in range(startExerciseRowId, exercisesSheet.nrows):
      exoStatus = 0
      exoToGen = 0
      exoId = exercisesSheet.cell(rx, 1).value
      exoId = exoId.encode("iso-8859-1")
      if exercisesSheet.cell(rx, cx+1).ctype == xlrd.XL_CELL_NUMBER:
        exoStatus =  int(exercisesSheet.cell(rx, cx+1).value)
      if exercisesSheet.cell(rx, cx).ctype == xlrd.XL_CELL_NUMBER:
        exoToGen =  int(exercisesSheet.cell(rx, cx).value)
#       print exoId, exoStatus, exoToGen
      exerciseStatus = ExerciseStatus(exoId, exoStatus, exoToGen)
      exerciseStatuses[exoId] = exerciseStatus
    studentsExercisesStatus.append(StudentExercicesStatus(studentId, comment, shouldGenerate, exerciseStatuses))
  return ClassStatus(students, studentsExercisesStatus)


if __name__ == "__main__":
  classStatus = parse(sys.argv[1])
  print str(len(classStatus.studentExercicesStatus)) + " student(s) exercices status"
