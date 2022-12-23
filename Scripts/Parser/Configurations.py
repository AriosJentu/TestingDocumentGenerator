import json
import os

from Scripts import Functions
from Scripts import Globals
from Scripts.Parser import Modules

class Configuration:
	'''
	Configuration - class working with configurations in JSON formats
	Can read, update and generate specific configurations
	'''

	DEFAULT_PATH = Functions.Path(
		"Configurations/DefaultModuleConfiguration.json"
	)

	DEFAULT_CONFIGURATION_FILENAME = "Configuration.json"

	def __init__(self, path: Functions.Path):
		self.configuration_path = path
		self.configuration = Functions.Struct()

	#@Readers
	def read_configuration(self):
		'''
		Function reads configurations in specified path, if it exists
		or, if it's not, it generates default configuration.
		Readin configuration from JSON and then convert it into Struct to
		easily access to variables without syntax calling dictionary element
		'''

		if not Functions.Path.isfile(str(self.configuration_path)):
			self.generate_default_configuration()

		with open(str(self.configuration_path), "r") as configuration:
			json_as_dict = json.loads(configuration.read())
			self.configuration.add_dict(json_as_dict)


	#@Setters
	def set_configuration(self, configuration: Functions.Struct):
		'''Function sets this object configuration from struct'''
		self.configuration = configuration


	def update_configuration(self):
		'''Function updates configuration from existed Struct configuration'''
		with open(str(self.configuration_path), "w") as configuration:
			converted_dict = json.dumps(self.configuration.dict(), indent=4)
			configuration.write(converted_dict)

	#@Getters
	def get_configuration(self) -> Functions.Struct:
		return self.configuration


	@staticmethod
	def get_default_configuration() -> 'Configuration':
		return Configuration(Configuration.DEFAULT_PATH)


	#@Generators
	def generate_default_configuration(self):
		'''
		Function generates default configuration from existed in specific path
		'''

		default_configuration = Configuration.get_default_configuration()
		default_configuration.read_configuration()
		self.set_configuration(default_configuration.get_configuration())
		self.update_configuration()

	#@Override
	def __str__(self):
		return f"{str(self.configuration_path)}[{str(self.configuration)}]"

	def __repr__(self):
		return self.__str__()

class CurrentConfiguration(Configuration):
	'''
	CurrentConfiguration - class works with configurations of current module
	'''

	#@Setters
	@staticmethod
	def set_current_configuration(configuration: Configuration):
		'''Function to set current configuration object'''
		Globals.CurrentConfiguration = configuration

	#@Getters
	@staticmethod
	def get_current_configuration() -> Configuration:
		'''Function to get current configuration object'''
		return Globals.CurrentConfiguration

	@staticmethod
	def get_current_module_configuration() -> Configuration:
		'''Function to get current module configuration'''
		current_module_path = Modules.CurrentModule.get_current_module_path()

		path = Functions.Path.join(
			current_module_path, Configuration.DEFAULT_CONFIGURATION_FILENAME
		)

		return Configuration(path)

	@staticmethod
	def clear_current_configuration():
		'''Function to clear current configuration object'''
		Globals.CurrentConfiguration = None
