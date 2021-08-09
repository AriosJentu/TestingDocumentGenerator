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
		'''
		Function to real Modules folder for modules
		Modules will be import, also sets variable 'MODULE_PATH'
		After imports, current_module will be cleared
		It must imply that every module has it's own variable of MODULE_PATH
		'''

		#For all directories in Modules folder
		for directory in Functions.Path.list_dirs(self.MODULES_DIRECTORY):
			
			#Add folder as module
			module = Module(Functions.Path.join(
				self.MODULES_DIRECTORY, 
				directory
			))

			#If this folder can be read as Module
			if module.is_module():
				#Firstly - save this module as current
				CurrentModule.set_current_module(module)

				#Import it:
				module.import_module()
				self.modules.append(module)

		#Then clear current module
		CurrentModule.clear_current_module()


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

		else: 
			#If there is no module, raise exception
			raise Functions.TestingException(
				Functions.TestingException.NoModule
			)


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


class CurrentModule:
	'''
	CurrentModule - class to get and set information about current module 
		in use.
	It will create simple hidden directory with information file,
		which will be loaded with the same class
	'''
	DIR_NAME = ".info"
	FILE_NAME = "module"

	@staticmethod
	def openfile(mode="r"):
		return open(
			Functions.Path.join(
				CurrentModule.DIR_NAME, 
				CurrentModule.FILE_NAME
			), 
		mode)

	@staticmethod
	def set_current_module(module: Module):
		'''Function to set current module'''
		Functions.Path.makedir_if_not_exists(CurrentModule.DIR_NAME)
		with CurrentModule.openfile("w") as file:
			file.write(module.path)

	@staticmethod
	def get_current_module_path() -> str:
		'''Function to get current module'''
		with CurrentModule.openfile() as file:
			return file.read()

	@staticmethod
	def clear_current_module():
		'''Function to clear current module'''
		with CurrentModule.openfile("w") as file:
			file.write("")

