import Scripts.Generators.Tasks as Tasks
import Scripts.Generators.Excercises as Excercises

def task1_update_task(string):
	return "Hello World" if string == "4" else string

task1 = Tasks.BasicTasks("Tasks/test.tex")
task1.set_updater_function(task1_update_task)
task1.read_information()
# for i in range(20):
# 	print(task1.generate_task())

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
# for i in range(24):
# 	print(repr(task2.generate_task()), [i.get_possible_appear_count() for i in task2variants])

task1_information = Tasks.TasksInformation(task1, 3)
task2_information = Tasks.TasksInformation(task2)

def excercise_update_title(string):
	return string.replace("world", "There")

excercise = Excercises.Excercise([task1_information, task2_information], "Hello world")
excercise.set_title_updater_function(excercise_update_title)

generated = excercise.generate_tasks()
generated.shuffle_tasks()
print(generated)
for task in generated:
	print(task)