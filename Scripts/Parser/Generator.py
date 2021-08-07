from ..Generators import Entries

from . import Parser
from . import Modules
from . import Arguments

from .. import EntryStudents
from .. import Assignments
from .. import Functions

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
	- 'is_all_tasks': Key for creating all available tasks in files (for debug, if True - generate ALL tasks from files, by default it's False - generate tasks as default)
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
		self.is_all_tasks = False

	def set_filename(self, filename):
		self.filename = filename

	def set_fileextension(self, fileextension):
		self.fileextension = fileextension

	def set_all_tasks_generation(self, is_all_tasks: bool = False):
		'''Function to set variable of generating all tasks'''
		self.is_all_tasks = is_all_tasks

	def set_separated(self, separated: bool = False):
		'''Function to set separation of the documents'''
		self.separated = separated

	def parse_arguments(self) -> Arguments.ArgumentsParser:
		'''Function to parse available arguments. Must be overloaded'''
		pass

	def read_assignments_list(self, info_module: Modules.Module):
		'''Function to generate object of class AssignmentsList from arguments parser for this class. 'info_module' must be a object of Module class with AssignmentsInformation object, which is an object of 'AssignmentsInformationClass' class'''

		if not isinstance(info_module, Modules.Module):
			return Functions.TestingException(Functions.TestingException.NoModule)

		argsparser = self.parse_arguments()

		assignments_kn = argsparser.parse_assignments_keynumbers()
		entries = argsparser.parse_entries()

		assignments = []
		#For all keynumbers for assignments
		for keynumbers in assignments_kn:

			#For all numbers from keynumbers for this assignment
			for number in keynumbers:

				#If this class exists
				if assignment_class := info_module.module.AssignmentsInformation.get(keynumbers.key, number):

					#Generate object of this class, set it's entries, and append to assignments list
					assignment = assignment_class()
					assignment.set_entries(entries)
					assignment.set_module(info_module)
					assignments.append(assignment)

		#Then generate object of class AssignmentsList from this assignments, and add module prefix for this
		self.assignments_list = Assignments.AssignmentsList(assignments)
		self.assignments_list.add_prefix_path(info_module.path)

	def generate(self, with_prefix: bool = True) -> [list[str], None]:
		'''Function to generate document from this assignment list'''
		return self.assignments_list.generate(
			self.filename+self.fileextension, 
			with_prefix, 
			self.separated, 
			self.is_all_tasks
		)

class GeneratorWithStudents(Generator):
	'''
	GeneratorWithStudents - child class of Generator class, which can parse arguments in way of students.
	'''
	def parse_arguments(self) -> Arguments.ArgumentsParser:
		'''Function to parse arguments with students classes'''

		#Read arguments
		args = Functions.Functions.crop_list_size(self.arguments, 8)[1:]

		#Parse arguments for separated
		if "-s" in args:
			self.set_separated(True)
			args.pop(args.index("-s"))

		#Parse arguments for all tasks
		if "-a" in args:
			self.set_all_tasks_generation(True)
			args.pop(args.index("-a"))

		#Keys must be 1st argument, after script name, entries must be 2nd argument
		keys = args[1]
		
		#If it's all tasks, doesn't matter which entries to generate
		if self.is_all_tasks:
			entries_obj = Entries.JoinedEntries()
			entries_obj.append(EntryStudents.StudentFromValues({"student": "Sample element", "group": "Sample group"}))

		#If it's not all tasks
		else:
			entries_list = args[2].split(";")

			entries_obj = Entries.JoinedEntries()

			for entries in entries_list:
				
				#If entries are not filepath, and not decimal, then suppose that this is student name
				if entries and not Functions.Path.isfile(entries) and not entries.isdecimal():
					#If this is student name, suppose next argument will be group name
					group = args[3] or "Group Name"
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
