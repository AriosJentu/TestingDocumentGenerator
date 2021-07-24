from .Generators import Tests
from .Generators import Entries
from .Generators import Documents
from .Generators import Functional

class Assignment:
	'''
	Assignment - parent class to work with assignments, containing all information about them. 
	Must contain default values for next parameters:
	- 'layout' - 'DocumentLayout' with information about document path and replacement string, and it's PageStyle
	- 'test' - 'Test' with it's 'Excercises', 
	- 'entries' - 'Entries' with their 'generate_information' method. This value can't be default, because it's generating by user's asking. For this situation exist method 'set_entries'
	- 'document_entry' - 'Struct' with additional information, which presented in pagestyle excercises format string. This argument may not be presented in class, by default it's empty entry
	- 'generation_folder' - String with folder name where generated files will be posted. By default it's 'Generated/' folder, but can be empty.
	Can be read in that order:
	Specific document 'layout' for every page must contain format of 'test' for every possible 'entries'. Every document must contain it's own default 'document_entries', which just appends to every entry.
	This class contain only one method, which generated by default, and won't to be edited. This method called every time when user asks to generate document.
	Every child class of this must replace only this available parameters to default values for specific kind of documents. Then this class must be appended in all classes list.
	'''

	layout: Documents.DocumentLayout
	test: Tests.Test
	entries: Entries.EntriesReader
	document_entry: Functional.Struct = Functional.Struct()
	generation_folder: str = "Generated/"

	def set_entries(self, entries: Entries.EntriesReader):
		self.entries = entries

	def generate(self, output_file: str = None):
		'''Function to generate Assignment document for various 'entries'. Working only with available parameters. If there is no output, function returns string of all document'''

		#First of all, generate entries elements
		entries_elements = self.entries.generate_information()

		#For all tests, read tasks
		for excercise in self.test.get_excercises():
			for tasks_information in excercise.get_tasks_information_list():
				tasks_information.get_tasks().read_information()


		#When entries are ready, generate information about pages:
		pages_information = Documents.PagesInformation()

		#Then, generate page value for all pages, which in common will be pages information
		for entry in entries_elements:
			#Construct page values from current entry information and all document entry information, and add them class of Test format
			page_values = Documents.PageValues(
				**entry.dict(), 
				**self.document_entry.dict(), 
				test_option=self.test
			)
			#Append this page value into pages information
			pages_information.append(page_values) 

		#Then generate Document object with containing pages information
		document = Documents.Document(self.layout, pages_information)
			
		#If there is no output file, return just string
		if not output_file:
			return document.generate_document_string()
		else:
			#Otherwice generate document on path
			document.generate_document(self.generation_folder+output_file)

