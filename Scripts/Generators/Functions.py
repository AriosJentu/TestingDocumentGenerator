import random

class Functions:

	@staticmethod
	def is_empty_string(string) -> bool:
		'''Function to check is string empty or is it starts from a comment operator (% for LaTeX)'''
		return string[0] == "%" or string == "" or string == " "

	@staticmethod
	def get_unused_index(from_list: list, cache_list: list) -> int:
		'''Function to get random index from unused tasks, and this index isn't appeared in cache'''
		random.seed()
		randindex = random.randrange(len(from_list))

		#If this element in cache already, then choose another element again
		if from_list[randindex] in cache_list:
			return Functions.get_unused_index(from_list, cache_list)
		else:
			return randindex