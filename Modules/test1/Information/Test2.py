from Modules import Imports

#Assignment part variables
prefix = "Information/Tasks/Test1/"
control_event = "Homework"
event_number = 2

#Layout part variables
test_format = "\t\\generatepage{{{control_event} \\#{event_number}}}{{{student}}}{{{group}}}{{\n{excercises}\n\t}}\n"
excercise_format = "\t\t\\item {title}\n{tasks}"
tasks_format = "\n\t\t\t{task}" 

#Layout location variable
layout_location = "Information/Layouts/sample.tex"

#Page style variable
page_style = Imports.Documents.PageStyle(test_format, excercise_format, tasks_format)

#Tasks update functions
def tasks1_update_task(string):
	return "Hello World "+string if string.find("4") >= 0 else string

def tasks3p4_update_task(string):
	return string.replace("Task", "Updated Task")

#Excercise update functions
def excercise1_update_title_function(string):
	return "Excercise "+string

#Configuration of the tasks:
#First task will be single basic task, with updater function
tasks1 = Imports.Tasks.BasicTasks(prefix+"tasks1.tex")
tasks1.set_updater_function(tasks1_update_task)

#Second task contain two basic tasks, task3 will be repeated twice
tasks2p1 = Imports.Tasks.BasicTasks(prefix+"tasks2.tex")
tasks2p2 = Imports.Tasks.BasicTasks(prefix+"tasks3.tex")

tasks2 = Imports.Tasks.MultiTasks([tasks2p1, tasks2p2])

#Third task will be specific task
tasks3 = Imports.Tasks.SpecificTasks()
for i in range(7):
	appearing_count = -1
	if i in [1, 2]:
		appearing_count = 2

	task = Imports.Tasks.SpecificTaskInfo(prefix+f"Special/variant{i+1}.tex", appearing_count)
	if i == 4:
		task.set_updater_function(tasks3p4_update_task)
	
	tasks3.append(task)

#Generate information arrays for the tasks, with repeatings
tasks1info = [Imports.Tasks.TasksInformation(tasks1)]
tasks2info = [Imports.Tasks.TasksInformation(tasks2, 3)]
tasks3info = [Imports.Tasks.TasksInformation(tasks3)]

#Generate excercises with this tasks information
excercise1 = Imports.Excercises.Excercise(tasks1info,
	title="1 -- Single task")
excercise2 = Imports.Excercises.Excercise(tasks2info,
	title="Excercise 2 -- two tasks with repeating (3 tasks in summary)")
excercise3 = Imports.Excercises.Excercise(tasks3info)

#Third task doesn't need to have title, but it's possible
#Shuffle 2nd excercise's tasks, and set title updater function for 1st excercise
excercise1.set_title_updater_function(excercise1_update_title_function)
excercise2.set_shuffle_state(True)

#Generate Assignment class for this Test assignment
class Test2(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(layout_location, page_style)
	test = Imports.Tests.Test([excercise1, excercise2, excercise3])
	document_entry = Imports.Functions.Struct(control_event=control_event, event_number=event_number)
	prefix = "tests"
	number = event_number
