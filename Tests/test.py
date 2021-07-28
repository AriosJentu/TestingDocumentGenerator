from ..Scripts.Generators import Tasks
from ..Scripts.Generators import Excercises
from ..Scripts.Generators import Tests
from ..Scripts.Generators import Documents
from ..Scripts.Generators import Functional
from ..Scripts import EntryStudents

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
		test_log(struct)

	test_log()

	structlist2 = Functional.StructList()
	structlist2.append(z)

	for struct in structlist2:
		test_log(struct)

	test_log(structlist1)
	test_log(structlist2)
	test_log(structlist1 == structlist2)

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
	def task2test5_update_task(string):
		return string.replace("Task", "Updated Task")

	task2tasks = []

	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant1.tex"))
	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant2.tex", 2))
	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant3.tex", 2))
	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant4.tex"))
	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant5.tex"))
	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant6.tex"))
	task2tasks.append(Tasks.SpecificTaskInfo("Tasks/Special/variant7.tex"))

	task2tasks[4].set_updater_function(task2test5_update_task)

	task2 = Tasks.SpecificTasks(task2tasks)
	task2.read_information()
	for i in range(24):
		test_log(repr(task2.generate_task()), [i.get_possible_appear_count() for i in task2tasks])

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

def test_testoption(excercise):
	testoption = Tests.Test([excercise, excercise])
	generated = testoption.generate_test()
	
	for excercise in generated:
		test_log(excercise)

	return testoption

def test_parse_arguments_class(testoption):
	pageargs = Documents.PageValues(group="M0744-228.13.37", student="AriosJentu", control_event="Homework", event_number=1, test_option=testoption)
	
	test_log(*pageargs)
	test_log(pageargs.dict())
	test_log(pageargs.get_test())
	
	return pageargs

def test_generate_pagestyle():

	test_format = "\t\\generatepage{{{control_event}}} #{{{event_number}}}{{{student}}}{{{group}}}{{\n{excercises}\n\t}}\n"
	excercise_format = "\t\t\\item {title}\n{tasks}"
	tasks_format = "\n\t\t\t{task}" 

	pagestyle = Documents.PageStyle(test_format, excercise_format, tasks_format)
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

def test_generate_students_with_tests_pagesinfo(students, testoption):
	
	pagesinfolist = Documents.PagesInformation()

	for student in students:
		pagevalue = Documents.PageValues(**student.dict(), control_event="Homework", event_number=1, test_option=testoption)
		pagesinfolist.append(pagevalue)

	return pagesinfolist

def test_generate_document_string(pagestyle, pagesinfo):

	document_layout = Documents.DocumentLayout("Layouts/sample.tex", pagestyle)

	document = Documents.Document(document_layout, pagesinfo)
	test_log(document.generate_document_string())

	return document

def test_generate_document(document):
	document.generate_document("Generated/generated.tex")

def run_test()
	# test_structs()
	task1 = test_task1()
	task2 = test_task2()
	task1_information, task2_information = test_task_information(task1, task2)
	excercise = test_excercises(task1_information, task2_information)
	testoption = test_testoption(excercise)
	pageargs = test_parse_arguments_class(testoption)
	students = test_students_reader()
	pagestyle = test_generate_pagestyle()
	pagesinfo = test_generate_students_with_tests_pagesinfo(students, testoption)
	test_generate_page(pagestyle, pageargs)
	document = test_generate_document_string(pagestyle, pagesinfo)
	test_generate_document(document)