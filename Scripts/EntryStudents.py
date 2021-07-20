from .Generators import Entries
from .Generators import Functional

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
