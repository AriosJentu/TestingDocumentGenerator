import Scripts.Generators.Tasks as Tasks
import Scripts.Generators.Excercises as Excercises
import Scripts.Generators.Tests as Tests
import Scripts.Generators.Documents as Documents
import Scripts.Generators.Functional as Functional
import Scripts.EntryStudents as EntryStudents
import Scripts.Assignments as Assignments

#Document part variables
layout_location = "Layouts/sample.tex"
control_event = "Homework"
event_number = 1

test_format = "\t\\generatepage{{{control_event} \\#{event_number}}}{{{student}}}{{{group}}}{{\n{excercises}\n\t}}\n"
excercise_format = "\t\t\\item {title}\n{tasks}"
tasks_format = "\n\t\t\t{task}" 

pagestyle = Documents.PageStyle(test_format, excercise_format, tasks_format)

#Entries variables
students_location = "Information/Students/students.txt"
students_entries = EntryStudents.StudentsReader(students_location)

#Tasks information
def task1_update_task(string):
	return "Hello World 4" if string == "4" else string

def task2test5_update_task(string):
	return string.replace("Task", "Updated Task")

task1 = Tasks.BasicTasks("Information/Tasks/Test1/tasks1.tex")
task1.set_updater_function(task1_update_task)

task2 = Tasks.SpecificTasks()
for i in range(7):
	
	appearing_count = -1
	if i == 1 or i == 2:
		appearing_count = 2

	task = Tasks.SpecificTaskInfo(f"Information/Tasks/Test1/Special/variant{i+1}.tex", appearing_count)
	if i == 4:
		task.set_updater_function(task2test5_update_task)
	
	task2.append(task)

task1info = Tasks.TasksInformation(task1, 3)
task2info = Tasks.TasksInformation(task2)

#Excercises information
excercise1 = Excercises.Excercise([task1info], "Excercise 1 -- look at three given tasks")
excercise2 = Excercises.Excercise([task2info], "Excercise 2 -- look at this specific tasks")

class DemontrativeWork(Assignments.Assignment):

	layout = Documents.DocumentLayout(layout_location, pagestyle)
	test = Tests.Test([excercise1, excercise2])
	document_entry = Functional.Struct(control_event=control_event, event_number=event_number)
	prefix = "sample"

work = DemontrativeWork()
work.set_entries(students_entries)
work.generate("generated.tex")