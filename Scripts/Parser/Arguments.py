from Scripts import Functions

from Scripts.Generators import Entries
from Scripts.Parser import Parser

class ArgumentsParser:
	'''
	ArgumentsParser - class to parse arguments to generate tasks
	Initial arguments:
	- 'keys': string in assignment-string values format 
		(like 'l1-4,7' etc, presented in Parser module)
	- 'entries': string/int/dictionary/Entries argument. 
		If string, it may be a filepath of the entries, or one of the 
		entry name (for example, student, if filepath not found). 
		If int, it may be count of generated specifically entries, 
		with case 'no file'. 
	'''

	def __init__(self, 
			keys: str, 
			entries: (str, int, dict, Entries.Entries), 
			*args, **kwargs
	):
		#If entries not intance of presented classes, then just make 
		# it empty, then it will generate entries without path
		if not isinstance(entries, (str, int, dict, Entries.Entries)):
			entries = None

		self.keys = keys
		self.entries = entries

		#Set classes as parameters of the class
		self.entries_with_path = Entries.EntriesReader
		self.entries_no_path = Entries.Entries
		self.entries_from_values = Entries.EntryFromValues


	#@Setters
	def set_entries_class(self, 
			with_path = Entries.EntriesReader, 
			no_path = Entries.Entries, 
			from_values = Entries.EntryFromValues
	):
		'''
		Function to update entries class - with_path, no_path and from_values
		'''
		self.entries_with_path = with_path
		self.entries_no_path = no_path
		self.entries_from_values = from_values


	#@Getters
	def parse_assignments_keynumbers(self) -> list[Parser.KeyNumbers]:
		'''Function to parse keys'''
		return Parser.Parser.parse_assignments_argument(self.keys)


	def parse_entries(self, entries=None) -> Entries.Entries:
		'''
		Function to parse entries. Will be recursive if entries are 
			list of joined, and argument needed to be in this situations
		'''
	
		#By default, if there is no arguments
		if not entries:
			#Set entries as entries element of this object
			entries = self.entries

		#If this is list of entries
		if isinstance(entries, Entries.JoinedEntries):
			joined_parsed = Entries.JoinedEntries()

			#For all entries inside, parse them recurselivly
			for entries_element in entries:
				joined_parsed.append(self.parse_entries(entries_element))

			#Return joined entries which are parsed
			return joined_parsed

		#If this path exists
		if isinstance(entries, str) and Functions.Path.isfile(entries):
			#Return entries with reading file
			return self.entries_with_path(entries)

		#If type of entries is dictionary
		if isinstance(entries, dict):
			#Generate struct list from this dictionary
			return self.entries_from_values(entries)
			
		#If type of entries is class Entries
		if isinstance(entries, Entries.Entries):
			#Return itself
			return entries

		#If there is no pattern for this element, just return empty struct:
		return self.entries_no_path()
