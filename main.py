from sys import argv

import Scripts.Main as Main
import Scripts.Globals as Globals
Globals.Initialize()

Globals.AvailableLogging["logging"] = True

def generate(args, current_module):
	import Scripts.Parser.Generator as Generator

	generator = Generator.GeneratorWithStudents(args)
	generator.read_assignments_list(current_module)
	generator.generate()
	
	return generator

if __name__ == "__main__":

	modules = Main.load_all_modules()
	
	default_configuration = Main.load_default_configuration()
	current_module = Main.load_current_module(modules, argv[1])
	
	Main.load_current_configurations(default_configuration)
	Main.import_current_module()

	generator = generate(argv, current_module)
	# print(generator.get_log())
	
	Main.clear()
	