from .Generators import Entries
from .Generators import Functional

class EmptyStudents(Entries.Entries):
	'''
	EmptyStudents - class with generating struct with specific entries count based on class parameter. No need to open files
	'''

	def generate_information(self) -> Functional.StructList:
		'''Function to generate information with StudentsReader-like pattern'''

		structs = Functional.StructList()
		for index in range(self.ENTRIES_COUNT):
			structs.append(Functional.Struct(student=f"A{index+1}", group="Sample group name"))

		return structs

class StudentsReader(Entries.EntriesReader):
	'''
	StudentsReader - class with reading information about students in specific format
	First line of the file is Group Number (or Group Name), all next lines after first are Student Names (list of students)
	Initial arguments:
	- 'filepath': Path of the students file
	'''

	def generate_information(self) -> Functional.StructList:
		'''Function to generate information. Pattern: fist line is 'group' string, all next lines are 'student' names'''
		lines = self.readlines()

		structs = Functional.StructList()
		for line in lines[1:]:
			if not Functional.Functions.is_empty_string(line):
				structs.append(Functional.Struct(student=line, group=lines[0]))

		return structs