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
  assert len(classStatus.students) == 33
  assert len(classStatus.studentExercicesStatus) == 33
  assert classStatus.studentExercicesStatus[0].studentId == "adeleide"
  assert classStatus.studentExercicesStatus[0].comment == None
  assert classStatus.studentExercicesStatus[0].shouldGenerate == True
  assert classStatus.studentExercicesStatus[0].exerciseStatuses['id2'].status == 2
  assert classStatus.studentExercicesStatus[0].exerciseStatuses['id2'].toGenerate == 0

  assert classStatus.studentExercicesStatus[10].studentId == "johannes"
  assert classStatus.studentExercicesStatus[10].comment == ur'Pass p\u00e5 \u00e5 \u00f8ve med operasjoner med negative tall og parenteser '
  print classStatus.studentExercicesStatus[10].exerciseStatuses['id2']
  assert classStatus.studentExercicesStatus[10].exerciseStatuses['id2'].status == 1
  assert classStatus.studentExercicesStatus[10].exerciseStatuses['id2'].toGenerate == 4

  assert classStatus.studentExercicesStatus[1].studentId == "anders"
  assert classStatus.studentExercicesStatus[1].shouldGenerate == False
