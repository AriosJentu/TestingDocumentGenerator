from ..Generators import Functional
from ..Generators import Entries
from . import Parser

class ArgumentsParser:
	'''
	ArgumentsParser - class to parse arguments to generate tasks
	Initial arguments:
	- 'keys': string in assignment-string values format (like 'l1-4,7' etc, presented in Parser module)
	- 'entries': string/int/dictionary/Entries argument. If string, it may be a filepath of the entries, or one of the entry name (for example, student, if filepath not found). If int, it may be count of generated specifically entries, with case 'no file'. 
	'''

	def __init__(self, keys: str, entries: (str, int, dict, Entries.Entries), *args, **kwargs):

		#If entries not intance of presented classes, then just make it empty, then it will generate entries without path
		if not isinstance(entries, (str, int, dict, Entries.Entries)):
			entries = None

		self.keys = keys
		self.entries = entries

		#Set classes as parameters of the class
		self.entries_with_path = Entries.EntriesReader
		self.entries_no_path = Entries.Entries
		self.entries_from_values = Entries.EntryFromValues

	def set_entries_class(self, with_path = Entries.EntriesReader, no_path = Entries.Entries, from_values = Entries.EntryFromValues):
		'''Function to update entries class - with_path, no_path and from_values'''
		self.entries_with_path = with_path
		self.entries_no_path = no_path
		self.entries_from_values = from_values

	def parse_assignments_keynumbers(self) -> list[Parser.KeyNumbers]:
		'''Function to parse keys'''
		return Parser.Parser.parse_assignments_argument(self.keys)

	def parse_entries(self) -> Entries.Entries:
		'''Function to parse entries'''

		#If this path exists, return entries with reading file
		if isinstance(self.entries, str) and Functional.Path.isfile(self.entries):
			entries = self.entries_with_path(self.entries)
			return entries

		#If type of entries is dictionary, then generate struct list from this dictionary
		if isinstance(self.entries, dict):
			entries = self.entries_from_values(self.entries)
			return entries

		#If this is integer, return entries without filepath with count of entries
		if isinstance(self.entries, int) or (isinstance(self.entries, str) and self.entries.isdecimal()):
			entries = self.entries_no_path()
			entries.ENTRIES_COUNT = int(self.entries)
			return entries
			
		#If type of entries is class Entries, then return itself
		if isinstance(self.entries, Entries.Entries):
			return self.entries

		#If there is no pattern for this element, just return empty struct:
		return self.entries_no_path()


