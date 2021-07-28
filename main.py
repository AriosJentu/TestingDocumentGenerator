from sys import argv
import Scripts.Parser.Generator as Generator

if __name__ == "__main__":
	generator = Generator.GeneratorWithStudents(argv)
	generator.read_assignments_list()
	generator.generate()
	print(generator.filename)