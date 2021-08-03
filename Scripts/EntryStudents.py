from .Generators import Entries

from . import Functions

class EmptyStudents(Entries.Entries):
	'''
	EmptyStudents - class with generating struct with specific entries count based on class parameter. No need to open files
	'''

	def generate_information(self) -> Functions.StructList:
		'''Function to generate information with StudentsReader-like pattern'''

		structs = Functions.StructList()
		for index in range(self.ENTRIES_COUNT):
			structs.append(Functions.Struct(student=f"A{index+1}", group="Sample group name"))

		return structs

	def get_group_name(self, default: str = None) -> str:
		if not default:
			default = f"n{self.ENTRIES_COUNT}students"
		return default

class StudentFromValues(Entries.EntryFromValues):
	'''
	StudentsFromValues - class with using information about students from struct
	Initial arguments:
	- 'element': dictionary or Struct of student format 
	'''

	def get_group_name(self, default: str = None) -> str:
		if not default:
			default = (self.element.group+"-"+self.element.student.split(" ")[0]).replace(" ", "_")
		return default

class StudentsReader(Entries.EntriesReader):
	'''
	StudentsReader - class with reading information about students in specific format
	First line of the file is Group Number (or Group Name), all next lines after first are Student Names (list of students)
	Initial arguments:
	- 'filepath': Path of the students file
	'''

	def generate_information(self) -> Functions.StructList:
		'''Function to generate information. Pattern: fist line is 'group' string, all next lines are 'student' names'''
		lines = self.readlines()

		structs = Functions.StructList()
		for line in lines[1:]:
			if not Functions.Functions.is_empty_string(line):
				structs.append(Functions.Struct(student=line, group=lines[0]))

		return structs

	def get_group_name(self, default: str = None) -> str:
		return self.readlines()[0]