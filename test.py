import Scripts.Generators.Tasks as Tasks
import Scripts.Generators.Excercises as Excercises
import Scripts.Generators.Variant as Variant
import Scripts.Generators.Document as Document
import Scripts.Generators.Functional as Functional
import Scripts.EntryStudents as EntryStudents

def test_log(*args, **kwargs):
	return
	# return print(*args, **kwargs)

def test_structs():
	
	x = Functional.Struct(a="1", b=2)
	y = Functional.Struct.from_struct(x)
	y.a = 12
	y.add(c=12)
	y.add(**{"d": 14})
	z = Functional.Struct(**{"c":"1", "d":2})

	test_log(x)
	test_log(x.dict())
	test_log(y)
	test_log(z)

	structlist1 = Functional.StructList()
	structlist1.append(x)
	structlist1.append(y)

	for struct in structlist1:
		print(struct)

	print()

	structlist2 = Functional.StructList()
	structlist2.append(z)

	for struct in structlist2:
		print(struct)

	print(structlist1)
	print(structlist2)
	print(structlist1 == structlist2)

def test_task1():
	def task1_update_task(string):
		return "Hello World" if string == "4" else string

	task1 = Tasks.BasicTasks("Tasks/test.tex")
	task1.set_updater_function(task1_update_task)
	task1.read_information()
	for i in range(20):
		test_log(task1.generate_task())

	return task1

def test_task2():
	def task2variant5_update_task(string):
		return string.replace("Task", "Updated Task")

	task2variants = []

	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant1.tex"))
	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant2.tex", 2))
	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant3.tex", 2))
	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant4.tex"))
	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant5.tex"))
	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant6.tex"))
	task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant7.tex"))

	task2variants[4].set_updater_function(task2variant5_update_task)

	task2 = Tasks.SpecificTasks(task2variants)
	task2.read_information()
	for i in range(24):
		test_log(repr(task2.generate_task()), [i.get_possible_appear_count() for i in task2variants])

	return task2

def test_task_information(task1, task2):
	task1_information = Tasks.TasksInformation(task1, 3)
	task2_information = Tasks.TasksInformation(task2)
	return task1_information, task2_information

def test_excercises(task1_information, task2_information):
	def excercise_update_title(string):
		return string.replace("world", "There")

	excercise = Excercises.Excercise([task1_information, task2_information], "Hello world")
	excercise.set_title_updater_function(excercise_update_title)

	generated = excercise.generate_tasks()
	generated.shuffle_tasks()
	test_log(generated)
	
	for task in generated:
		test_log(task)

	return excercise

def test_variant(excercise):
	variant = Variant.Variant([excercise, excercise])
	generated = variant.generate_variant()
	
	for excercise in generated:
		test_log(excercise)

	return variant

def test_parse_arguments_class(variant):
	pageargs = Document.PageValues(group="M0744-228.13.37", student="AriosJentu", control_event="Homework", variant=variant)
	
	test_log(*pageargs)
	test_log(pageargs.dict())
	test_log(pageargs.get_variant())
	
	return pageargs

def test_generate_pagestyle():

	page_format = "\t\\generatepage{{{control_event}}}{{{student}}}{{{group}}}{{\n{excercises}\n\t}}\n"
	excercise_format = "\t\t\\item {title}\n{tasks}"
	tasks_format = "\n\t\t\t{task}" 

	pagestyle = Document.PageStyle(page_format, excercise_format, tasks_format)
	return pagestyle


def test_generate_page(pagestyle, pageargs):
	
	page = pagestyle.generate_page(pageargs)
	test_log(page)

def test_students_reader():
	studreader = EntryStudents.StudentsReader("Information/Students/students.txt")
	students = studreader.generate_information()
	for student in students:
		test_log(student)

	return students

def test_generate_students_with_variants_pagesinfo(students, variant):
	
	pagesinfolist = Document.PagesInformation()

	for student in students:
		pagevalue = Document.PageValues(**student.dict(), control_event="Homework", variant=variant)
		pagesinfolist.append(pagevalue)

	return pagesinfolist

def test_generate_document_string(pagestyle, pagesinfo):

	document = Document.Document("Layouts/sample.tex", pagestyle, pagesinfo)
	test_log(document.generate_document_string())

	return document

def test_generate_document(document):
	document.generate_document("Generated/generated.tex")

def test_students_variant(students, variant):
	pass

# test_structs()
task1 = test_task1()
task2 = test_task2()
task1_information, task2_information = test_task_information(task1, task2)
excercise = test_excercises(task1_information, task2_information)
variant = test_variant(excercise)
pageargs = test_parse_arguments_class(variant)
students = test_students_reader()
pagestyle = test_generate_pagestyle()
pagesinfo = test_generate_students_with_variants_pagesinfo(students, variant)
test_generate_page(pagestyle, pageargs)
document = test_generate_document_string(pagestyle, pagesinfo)
test_generate_document(document)