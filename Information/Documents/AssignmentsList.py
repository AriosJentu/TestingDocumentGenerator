class AssignmentsListClass:
	'''
	AssignmentsListClass - class which contains information about generated labs.
	'''

	def __init__(self):
		self.dict = {}

	def append(self, assignment_class, key: str):
		'''Function to append assignment class into this module'''
		if self.dict.get(key) == None:
			self.dict[key] = {}

		#Append assignment with it's number inside class
		self.dict[key][1] = assignment_class

	def get(self, key: str, number: int):
		'''Function to get assignment with it's key and number'''
		if self.dict.get(key):
			return self.dict[key].get(number)

AssignmentsList = AssignmentsListClass()

#Imports 
from . import Test1

#Append assignment Test1 into Assignments List
AssignmentsList.append(Test1.Test1, "t")
