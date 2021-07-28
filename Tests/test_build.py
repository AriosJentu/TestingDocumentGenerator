from ..Information.Documents import AssignmentsInformation
from ..Scripts import EntryStudents
from ..Scripts import Assignments

def run_test()
	students_location = "Information/Students/students.txt"
	students_entries = EntryStudents.EmptyStudents()
	students_entries.ENTRIES_COUNT = 5

	Test1 = AssignmentsInformation.AssignmentsInformation.get("t", 1)
	Test2 = AssignmentsInformation.AssignmentsInformation.get("t", 2)

	work1 = Test1()
	work1.set_entries(students_entries)

	work2 = Test2()
	work2.set_entries(students_entries)

	assignments = Assignments.AssignmentsList()
	assignments.append(work1)
	assignments.append(work2)

	assignments.generate("document.tex")
		