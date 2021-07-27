import os.path
from ..Generators import Functional
from ..Generators import Entries
from . import Parser

class ArgumentsParser:
	'''
	ArgumentsParser - class to parse arguments to generate tasks
	Initial arguments:
	- 'keys': string in assignment-string values format (like 'l1-4,7' etc, presented in Parser module)
	- 'entries': string/int/dictionary argument. If string, it may be a filepath of the entries, or one of the entry name (for example, student, if filepath not found). If int, it may be count of generated specifically entries, with case 'no file'. 
	- 'group_string': string (may be empty) with group name, in case of specific student generator.
	'''

	def __init__(self, keys: str, entries: [str, int, dict, Functional.StructList], *args, **kwargs):

		if not isinstance(entries, (str, int, dict, Functional.StructList)):
			entries = {}

		self.keys = keys
		self.entries = entries
		self.group_string = group_string

	def parse_keys(self) -> (str, list[int]):
		'''Function to parse keys'''
		return Parser.parse_assignments_argument(self.keys)

	def parse_entries(self, entries_with_path = Entries.EntriesReader, entries_no_path = Entries.Entries) -> Functional.StructList:
		'''
		Function to parse entries.
		Arguments:
		- 'entries_with_path': class of generating entries with file reading options
		- 'entries_no_path': class of generating entries without reading, generate by count
		'''

		#If this path exists, return entries with reading file
		if os.path.isfile(self.entries):
			entries = entries_with_path(self.entries)
			return entries

		#If type of entries is dictionary, then generate struct list from this dictionary
		if isinstance(entries, dict):
			return Functional.StructList([Functional.Struct(**self.entries)])

		#If this is integer, return entries without filepath with count of entries
		if type(self.entries) == int or self.entries.isdecimal():
			entries = entries_no_path()
			entries.ENTRIES_COUNT = int(self.entries)
			return entries
			
		#If type of entries is struct list, then return itself
		if isinstance(entries, Functional.StructList):
			return entries

		#If there is no pattern for this element, just return empty struct:
		return entries_no_path()


