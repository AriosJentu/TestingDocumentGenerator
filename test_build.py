import Information.Documents.AssignmentsList as AssignmentsList
import Scripts.EntryStudents as EntryStudents

students_location = "Information/Students/students.txt"
students_entries = EntryStudents.EmptyStudents()
students_entries.ENTRIES_COUNT = 20

Test1 = AssignmentsList.AssignmentsList.get("t", 1)

work = Test1()
work.set_entries(students_entries)
work.generate("generated_new.tex")