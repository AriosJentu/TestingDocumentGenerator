from Scripts import Functions

class Module:
	'''
	Module - basic class with information about module for this project
	'''

	def __init__(self, main_path: str = ""):
		self.path = main_path
		self.infopath = Functions.Path.join(self.path, 
			"Information", "AssignmentsInformation.py"
		)
		self.modulepath = Functions.Path.replace_separator(self.infopath[:-3])
		self.module = None

	
	#@Setters
	def import_module(self):
		'''Function to import this module into code'''
		self.module = __import__(self.modulepath, fromlist=[None])


	#@Getters
	def is_module(self):
		'''
		Function to check is this module is a Module 
		(with existing it's inforpath file)
		'''
		return Functions.Path.isfile(self.infopath)


	#@Override
	def __str__(self):
		return "Module["+self.path+"]"

	def __repr__(self):
		return self.__str__()


class ModulesLoader:
	'''
	ModulesLoader - class which can load all possible modules 
		from Modules folder
	'''

	MODULES_DIRECTORY = "Modules"

	def __init__(self):
		self.modules = []


	#@Readers
	def read_modules(self):
		'''Function to real Modules folder for modules'''

		#For all directories in Modules folder
		for directory in Functions.Path.list_dirs(self.MODULES_DIRECTORY):
			
			#Add folder as module
			module = Module(Functions.Path.join(
				self.MODULES_DIRECTORY, 
				directory
			))

			#If this folder can be read as Module
			if module.is_module():
				#Import it
				module.import_module()
				self.modules.append(module)


	#@Getters
	def get_module(self, path: str):
		'''Function to get this module from it's name (path)'''
		for module in self.modules:
		
			check1 = (module.path == Functions.Path.join(
				self.MODULES_DIRECTORY, path
			))
		
			check2 = (module.path == path)

			#If module path is exists as Modules path or just name
			if check1 or check2:
				#Return this module
				return module


	#@Override
	def __iter__(self):
		for module in self.modules:
			yield module

	def __str__(self):
		return "ModulesLoader("+", ".join([
			str(module) for module in self.modules
		])+")"

	def __repr__(self):
		return self.__str__()
