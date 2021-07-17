import Scripts.Generators.Tasks as Tasks

task1 = Tasks.BasicTasks("Tasks/test.tex")
task1.read_information()
for i in range(20):
	print(task1.generate_task())

task2variants = []
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant1.tex"))
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant2.tex", 2))
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant3.tex", 2))
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant4.tex"))
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant5.tex"))
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant6.tex"))
task2variants.append(Tasks.SpecificTaskInfo("Tasks/Special/variant7.tex"))
task2 = Tasks.SpecificTasks(task2variants)
task2.read_information()
for i in range(24):
	print(task2.generate_task(), [i.get_possible_appear_count() for i in task2variants])