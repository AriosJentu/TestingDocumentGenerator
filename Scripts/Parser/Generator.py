import Information.Documents.AssignmentsInformation as AssignmentsInformation
from ..Generators import Functional
from ..Generators import Entries
from .. import EntryStudents

from . import Parser
from . import Arguments
from .. import Assignments

class Generator:
	'''
	Generator - parent class which can generate documents from script arguments.
	Contains next arguments:
	- 'arguments': list of arguments
	- 'kwarguments': dictionary with keyword arguments
	- 'assignments_list': list of assignments which will be generated with function 'generate', 
	- 'filename': string of basic filename (without extension)
	- 'fileextension': string of extension of the filename (by default - '.tex')
	- 'separated': boolean value which indicates separation of the simial type assignments (be default - False)
	Need to override function 'parse_arguments' when use this class as parent, by default function doesn't do nothing. This function must return object of ArgumentsParser class
	'''

	def __init__(self, *args, **kwargs):
		#Assume that arguments and kwarguments are list/dict with string values
		self.arguments = list(*args)
		self.kwarguments = dict(**kwargs)
		self.assignments_list = Assignments.AssignmentsList()
		self.filename = ""
		self.fileextension = ".tex"
		self.separated = False

	def set_filename(self, filename):
		self.filename = filename

	def set_fileextension(self, fileextension):
		self.fileextension = fileextension

	def parse_arguments(self) -> Arguments.ArgumentsParser:
		'''Function to parse available arguments. Must be overloaded'''
		pass

	def read_assignments_list(self):
		'''Function to generate object of class AssignmentsList from arguments parser for this class'''

		argsparser = self.parse_arguments()

		assignments_kn = argsparser.parse_assignments_keynumbers()
		entries = argsparser.parse_entries()

		assignments = []
		#For all keynumbers for assignments
		for keynumbers in assignments_kn:

			#For all numbers from keynumbers for this assignment
			for number in keynumbers:

				#If this class exists
				if assignment_class := AssignmentsInformation.AssignmentsInformation.get(keynumbers.key, number):

					#Generate object of this class, set it's entries, and append to assignments list
					assignment = assignment_class()
					assignment.set_entries(entries)
					assignments.append(assignment)

		#Then generate object of class AssignmentsList from this assignments
		self.assignments_list = Assignments.AssignmentsList(assignments)

	def generate(self, with_prefix: bool = True) -> [list[str], None]:
		'''Function to generate document from this assignment list'''
		return self.assignments_list.generate(self.filename+self.fileextension, with_prefix, self.separated)

class GeneratorWithStudents(Generator):
	'''
	GeneratorWithStudents - child class of Generator class, which can parse arguments in way of students.
	'''
	def parse_arguments(self) -> Arguments.ArgumentsParser:
		'''Function to parse arguments with students classes'''

		#Read arguments
		args = Functional.Functions.crop_list_size(self.arguments, 4)[1:]
		keys = args[0]
		entries_list = args[1].split(";")

		entries_obj = Entries.JoinedEntries()

		for entries in entries_list:
			
			#If entries are not filepath, and not decimal, then suppose that this is student name
			if entries and not Functional.Path.isfile(entries) and not entries.isdecimal():
				#If this is student name, suppose next argument will be group name
				group = args[2] or "Group Name"
				entries = EntryStudents.StudentFromValues({"student": entries, "group": group})

			#If entries are decimals, generate integer of decimals
			elif entries and entries.isdecimal():
				entries = int(entries)

			#This time may append not 'entries' element into JoinedEntries, but in parser it will be parsed 
			entries_obj.append(entries)

		#Generate argument parser with keys, entries, and Students Entries classes
		arguments_parser = Arguments.ArgumentsParser(keys, entries_obj)
		arguments_parser.set_entries_class(EntryStudents.StudentsReader, EntryStudents.EmptyStudents, EntryStudents.StudentFromValues)
		
		#Set filename with group names of all available entries:
		string = "_".join([entries.get_group_name() for entries in arguments_parser.parse_entries()])
		self.set_filename(string)

		return arguments_parser
