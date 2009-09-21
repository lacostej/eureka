import excelparse

TEST_DATA_DIR = "./tests/data/"

def setUp(self):
  pass

def tearDown(self):
  pass

def testReadExcelInterfaceFile():
  classStatus = excelparse.parse("data/interface.xls")

  print str(len(classStatus.students)) + " student(s)"
#  print str(len(classStatus.studentsExercises())) + " exercise(s)" 
  assert len(classStatus.students) == 33
   
