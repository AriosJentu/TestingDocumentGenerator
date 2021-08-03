from .. import Functions

class Module:
	'''
	Module - basic class with information about module for this project
	'''

	def __init__(self, main_path: str = ""):
		self.path = main_path
		self.infopath = Functions.Path.join(self.path, "Information", "AssignmentsInformation.py")
		self.modulepath = Functions.Path.replace_separator(self.infopath[:-3])
		self.module = None

	def is_module(self):
		return Functions.Path.isfile(self.infopath)

	def import_module(self):
		self.module = __import__(self.modulepath, fromlist=[None])

	def __str__(self):
		return "Module["+self.path+"]"

	def __repr__(self):
		return self.__str__()


class ModulesLoader:
	'''
	ModulesLoader - class which can load all possible modules from Modules folder
	'''

	MODULES_DIRECTORY = "Modules"

	def __init__(self):
		self.modules = []

	def read_modules(self):
		for directory in Functions.Path.list_dirs(self.MODULES_DIRECTORY):
			module = Module(Functions.Path.join(self.MODULES_DIRECTORY, directory))
			if module.is_module():
				module.import_module()
				self.modules.append(module)

	def get_module(self, path: str):
		for module in self.modules:
			check1 = (module.path == Functions.Path.join(self.MODULES_DIRECTORY, path))
			check2 = (module.path == path)
			if check1 or check2:
				return module

	def __iter__(self):
		for module in self.modules:
			yield module

	def __str__(self):
		return "ModulesLoader("+", ".join([str(module) for module in self.modules])+")"

	def __repr__(self):
		return self.__str__()
