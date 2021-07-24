import Information.Documents.Test1 as Test1

students_location = "Information/Students/students.txt"
students_entries = Test1.Imports.EntryStudents.StudentsReader(students_location)

work = Test1.Test1()
work.set_entries(students_entries)
work.generate("generated_new.tex")