from sys import argv
import Scripts.Globals as Globals
Globals.Initialize()

import Scripts.Parser.Modules as Modules
import Scripts.Parser.Configurations as Configurations
	
def load_all_modules():

	modules = Modules.ModulesLoader()
	modules.read_modules()

	return modules

def load_default_configuration():
	
	default_configuration = Configurations.Configuration.get_default_configuration()
	default_configuration.read_configuration()
	Configurations.CurrentConfiguration.set_current_configuration(default_configuration)

	return default_configuration

def load_current_module(modules, argument):

	current_module = modules.get_module(argument)
	Modules.CurrentModule.set_current_module(current_module)

	return current_module

def load_current_configurations(default_configuration):

	configuration = Configurations.CurrentConfiguration.get_current_module_configuration()
	configuration.set_configuration(default_configuration.get_configuration())
	configuration.read_configuration()
	Configurations.CurrentConfiguration.set_current_configuration(configuration)

def import_current_module():
	Modules.CurrentModule.import_module()

def generate(args, current_module):
	import Scripts.Parser.Generator as Generator

	generator = Generator.GeneratorWithStudents(args)
	generator.read_assignments_list(current_module)
	generator.generate()
	
	return generator

def clear():
	Modules.CurrentModule.clear_current_module()
	Configurations.CurrentConfiguration.clear_current_configuration()

if __name__ == "__main__":

	modules = load_all_modules()
	default_configuration = load_default_configuration()
	current_module = load_current_module(modules, argv[1])
	load_current_configurations(default_configuration)
	import_current_module()
	generator = generate(argv, current_module)
	print(generator.get_log())
	clear()
	