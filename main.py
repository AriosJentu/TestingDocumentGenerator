from sys import argv
import Scripts.Parser.Modules as Modules
import Scripts.Parser.Generator as Generator

modules = Modules.ModulesLoader()
modules.read_modules()

if __name__ == "__main__":
	current_module = modules.get_module(argv[1])
	Modules.CurrentModule.set_current_module(current_module)

	generator = Generator.GeneratorWithStudents(argv)
	generator.read_assignments_list(current_module)
	generator.generate()
	print(generator.get_log())

	Modules.CurrentModule.clear_current_module()