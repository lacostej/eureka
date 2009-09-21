import xlrd

class ClassStatus:

  def __init__(self, students, studentExercicesStatus):
    self.students = students
    self.studentExercicesStatus = studentExercicesStatus
    
class Student:
  def __init__(self, shortName, fullName, email):
    self.shortName = shortName
    self.fullName = fullName
    self.email = email


class StudentExercicesStatus:
  def student():
    return ""
  def studentExeri():
    return []


def parse(fileName):
  book = xlrd.open_workbook(fileName)
  print "worksheets", book.nsheets
  if (book.nsheets < 2):
    raise MyException("Number of sheets is invalid. We expect at least 2 sheets.")

  students = []
  studentSheet = book.sheet_by_index(0)
  print studentSheet.name, studentSheet.nrows, studentSheet.ncols
  if (studentSheet.ncols < 3): 
    raise MyException("Number of columns in sheet 1 '%s' is invalid. We expect 3 columns." & studentSheet.ncols)
  for rx in range(studentSheet.nrows):
    if (rx == 0):
      continue # skip header
    row = studentSheet.row(rx)
    students.append(Student(row[0].value, row[0].value, row[0].value))

  studentsExercisesStatus = []
  return ClassStatus(students, studentsExercisesStatus)

if __name__ == "__main__":
  classStatus = parse(sys.argv[1])
  print str(len(classStatus.studentExercicesStatus)) + " student(s) exercices status"

