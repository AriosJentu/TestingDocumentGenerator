from sys import argv
import Scripts.Parser.Modules as Modules
import Scripts.Parser.Generator as Generator

modules = Modules.ModulesLoader()
modules.read_modules()

if __name__ == "__main__":
	generator = Generator.GeneratorWithStudents(argv)
	generator.read_assignments_list(modules.get_module(argv[1]))
	generator.generate()
	print(generator.filename)