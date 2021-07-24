class Parser:
	'''
	Parser - static class with function to parse string of assignment arguments format.
	Main method: Parser.parse_assignments_argument(string). It parses strings in specific format with tasks ranges.
	For example. string "l1-3,5" will be parsed with 'key': 'l', and list of numbers: [1, 2, 3, 5]
	'''

	@staticmethod
	def is_valid_string(string) -> bool:
		'''Function to check is input string is in correct form'''
		string = string.replace("-", ",").replace(" ", "")
		values = string.split(",")
		return False not in [value.isdecimal() for value in values]

	@staticmethod
	def range_to_list(string) -> list[int]:
		'''Function to convert string ranges in form 'a-b' to list of values in this range [a, a+1, ..., b-1, b]. Also possible to parse single number 'a', in this case function returns [a]'''
		
		#If parsed string is invalid, then break
		if not Parser.is_valid_string(string) and string.find(",") >= 0:
			return None		

		values = [int(i) for i in string.split("-")]
		if len(values) > 1:
			values = list(range(values[0], values[-1]+1))

		return values

	@staticmethod
	def parse_assignments_argument(string) -> [str, list[int]]:
		'''
		Function to parse input string to find specific assignment documents with pattern.
		Pattern would prefer next form:
		"{assignment_key}{assignment_number}"
		- 'assignment_key' - single latin symbol which indicates specific series of the assignments (for example, suppose 't' indicate all test assignments)
		- 'assignment_number' - number of the assignment from specific series. Can contain one number: "t1", numbers as 'list': "t1,2,4", or range: "t1-4".
		Because of different layouts it's not perfrectly possible to generate different documents at one
		Input arguments:
		- 'string': String which would satisfie presented pattern
		Returns:
		- 'key': One char with key of argument
		- 'numbers': List of the parsed numbers which are satisfy this pattern
		'''

		#It's possible to make with regexp, I think, but I haven't any idea how to make it with regexp
		#Using basic idea - first char is key, next are numbers, in format "1", "1,2,3" or "1-4", also possible to use "1,2-4"

		key = string[0]
		
		#If next part of string is invalid, then return False
		if not Parser.is_valid_string(string[1:]):
			return False

		#Otherwise represent them as list of ranges, which are separated with comma
		ranges = string[1:].split(",")
		numbers = [index for irange in ranges for index in Parser.range_to_list(irange) if index is not None]

		#Return key and list of numbers
		return key, numbers
