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


def load_current_module(modules, module_name):

	current_module = modules.get_module(module_name)
	Modules.CurrentModule.set_current_module(current_module)

	return current_module


def load_current_configurations(default_configuration):

	configuration = Configurations.CurrentConfiguration.get_current_module_configuration()
	configuration.set_configuration(default_configuration.get_configuration())
	configuration.read_configuration()
	Configurations.CurrentConfiguration.set_current_configuration(configuration)


def import_current_module():
	Modules.CurrentModule.import_module()


def clear():
	Modules.CurrentModule.clear_current_module()
	Configurations.CurrentConfiguration.clear_current_configuration()
