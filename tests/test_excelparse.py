import excelparse

TEST_DATA_DIR = "./tests/data/"

def setUp(self):
  pass

def tearDown(self):
  pass

def testReadExcelInterfaceFile():
  classStatus = excelparse.parse("data/interface.xls")

  print str(len(classStatus.students)) + " student(s)"
  print str(len(classStatus.studentExercicesStatus)) + " exercise(s)" 
  assert len(classStatus.students) == 34
  assert len(classStatus.studentExercicesStatus) == 34
  assert classStatus.studentExercicesStatus[0].studentId == "adeleide"
  assert classStatus.studentExercicesStatus[0].uComment == None
  assert classStatus.studentExercicesStatus[0].shouldGenerate == False
  assert classStatus.studentExercicesStatus[0].exerciseStatuses['id2'].status == 2
  assert classStatus.studentExercicesStatus[0].exerciseStatuses['id2'].toGenerate == 0

  assert classStatus.studentExercicesStatus[10].studentId == "johannes"
  assert classStatus.studentExercicesStatus[10].uComment == ur'Pass p\u00e5 \u00e5 \u00f8ve med operasjoner med negative tall og parenteser '
  print classStatus.studentExercicesStatus[10].exerciseStatuses['id2']
  assert classStatus.studentExercicesStatus[10].exerciseStatuses['id2'].status == 1
  assert classStatus.studentExercicesStatus[10].exerciseStatuses['id2'].toGenerate == 4

#  print classStatus.studentExercicesStatus
  assert classStatus.studentExercicesStatus[33].studentId == "jerome"
  assert classStatus.studentExercicesStatus[33].shouldGenerate == True

  assert classStatus.email == False

def testReadExcelInterfaceFile2():
  classStatus = excelparse.parse("data/interface2.xls")
  assert classStatus.email == True

