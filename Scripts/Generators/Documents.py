from Scripts import Functions
from Scripts import Globals

from Scripts.Generators import Tests
from Scripts.Generators import Exercises
from Scripts.Parser import Modules

CurrentConfiguration = Globals.CurrentConfiguration.get_configuration()

class Page(str):
	'''Define Page class as string class'''
	pass


class Layout(str):
	'''Define Layout class as string class'''
	pass


class Content(str):
	'''Define Content class as string class'''
	pass


class PageValues(Functions.Struct):
	'''
	PageArguments - class with Struct format, working with dictionaries.
	Initial arguments:
	- 'test_option': Test option for this page (object of class Test) 
	- 'entries': Dictionary of values, which will be used in generation
	'''

	def __init__(self, 
			test_option: Tests.Test, 
			**entries
	):
		super().__init__(**entries)
		self.__test_option__ = test_option


	#@Getters
	def get_test(self) -> Tests.Test:
		return self.__test_option__


	#@Gemerators
	def generate_test(self) -> Tests.GeneratedTest:
		'''Function to generate test option from this format'''
		return self.__test_option__.generate_test()


class PagesInformation(Functions.StructList):
	'''
	PagesInformation - class which containing information about all available 
		pages
	Initial arguments:
	- 'structlist': list of object of PageValues class
	'''
	pass


class PageStyle:
	'''
	PageStyle - class with style information about page of document
	Inital arguments:
	- 'test_format_string': Format-type string with content of test option of 
		the page. Must containing {exercises} element to replace them with 
		exercises of the test, and some other text {arg1}, {arg2} from 
		executing PageValues class, etc. Will be used in context 
		of 'test_format_string.format(**format_arguments.dict(), 
		exercises="Some exercises")'
	- 'exercise_format_string': Format-type string for test. Must 
		containing {title} and {tasks} elements. Will be used in context 
		of 'exercise_format_string.format(title="Title", tasks="Some tasks")'
	- 'tasks_format_string': Format-type string for tasks. Must 
		containing {task} element. Will be used in context 
		of 'tasks_format_string.format(task="This task")'
	Available attributes:
	- 'test_option_format': Page format string
	- 'exercise_format': Exercises format string
	- 'tasks_format': Tasks format string
	- 'updater': Function which updates page after generating content
	'''

	def __init__(self, 
			test_format_string: str, 
			exercise_format_string: str,
			tasks_format_string: str = "{task}",
	):
		self.test_option_format = test_format_string
		self.exercise_format = exercise_format_string
		self.tasks_format = tasks_format_string
		self.updater = lambda text: text


	#Getters
	def __format_exercise__(self, 
			exercise: Exercises.GeneratedExercise
	) -> str:
		'''Function to format exercise'''

		#First of all - format all tasks of this exercise
		tasks_formatted = []

		for task in exercise:
			task_string = self.tasks_format.format(task=task.get_task())
			tasks_formatted.append(task_string)

		#Merge all tasks with new lines
		exercise_tasks = "\n".join(tasks_formatted)

		#For default exercise format string use PageStyle's format
		format_string = self.exercise_format

		#If for this exercise exist self formatting, use it as format string:
		if exercise.exercise_format:
			format_string = exercise.exercise_format

		#Format exercise with title and formated tasks
		return format_string.format(
			title=exercise.get_title(), 
			tasks=exercise_tasks
		)


	#Setters
	def set_page_content_updater_function(self, 
			updater_function = lambda taskstring: taskstring
	):
		'''
		Function for chanhing page content updater `function` after 
			generating content
		'''
		self.updater = updater_function


	#@Generators
	def generate_page(self, 
			format_arguments: PageValues, 
	) -> Page:
		'''
		Function to generate page string from format arguments and exercises. 
			Put all in format string and return it.
		Arguments:
		- 'format_arguments': Object of class PageValues. Containing page 
			arguments with test option with exercises
		'''

		#Generate test for this page from available test option format 
		# of PageValues object
		generated_test = format_arguments.generate_test()
		exercises_formatted = []
		
		#For all exercises from this generated test
		for exercise in generated_test:

			#Format exercise with title and formated tasks and add it in list 
			# of formatted exercises
			excersise_formatted = self.__format_exercise__(exercise)
			exercises_formatted.append(excersise_formatted)

		#Merge all exercises and put this content inside page
		page_exercises = "\n".join(exercises_formatted)
		page_content = self.test_option_format.format(
			**format_arguments.dict(), 
			exercises=page_exercises
		)

		#Update content after generating
		page_content = self.updater(page_content)

		return Page(page_content)


class DocumentLayout:
	'''
	DocumentLayout - class to work with document layout information
	Initial arguments:
	- 'layout_path': Path of the document layout. This layout need to 
		contain 'page_word' inside, will be replaced with generating page
	- 'page_style': Object of class PageStyle, which containing all 
		information about style of the page
	- 'content_string': Word in layout file, which will be replaced with 
		generation content. By default suppose to be "$CONTENT$"
	Available attributes:
	- 'layout': Document layout file path
	- 'pagestyle': Page style information object
	- 'contentstr': Content word in layout file
	'''
	def __init__(self, 
			layout_path: str,
			page_style: PageStyle,
			content_string: str = CurrentConfiguration.ContentString,
			module_path_string: str = CurrentConfiguration.ModuleString,
	):
		self.layout = layout_path
		self.pagestyle = page_style
		self.contentstr = content_string
		self.modulepathstr = module_path_string


	#@Setters
	def add_prefix_path(self, prefix_path: str):
		'''Function to add prefix path for layouts'''
		self.layout = Functions.Path.join(prefix_path, self.layout)

	def __replace_layout_module_path__(self, layout_str: str) -> str:
		modulepath = Modules.CurrentModule.get_current_module_path()
		return layout_str.replace(self.modulepathstr, modulepath)


	#@Getters
	def get_layout(self) -> Layout:
		'''Function to read document layout'''
		layout = ""
		with open(self.layout) as file:
			layout = file.read()

		#Replace module_path with path of module
		layout = self.__replace_layout_module_path__(layout)
		return Layout(layout)

	def get_document_string_wth_content(self, content: Content) -> str:
		'''Function to generate document with content from layout'''
		layout = self.get_layout()
		return layout.replace(self.contentstr, content)

	
	#@Generators	
	def generate_page(self, page_values: PageValues) -> Page:
		return self.pagestyle.generate_page(page_values)


class Document:
	'''
	Document - class to work with document using any information about it
	Inital arguments:
	- 'layout': Object of class DocumentLayout, which contains information 
		about document layout and it's content string
	- 'pages_info': Object of class PagesInformation, which containing all 
		information about generating page arguments and all generated 
		tasks for this arguments
	Available attributes:
	- 'layout': Document layout object
	- 'pagesinfo': List of informations about pages, objects 
		of PageValues class
	'''
	def __init__(self, 
			layout: DocumentLayout,
			pages_info: PagesInformation,
	):
		self.layout = layout
		self.pagesinfo = pages_info


	#@Generators
	def generate_content(self) -> Content:
		'''
		Function to generate pages content for document from available info
		'''
		
		document_content_list = []

		#For every page generate content
		for page_value in self.pagesinfo:
			
			page_content = self.layout.generate_page(page_value)
			document_content_list.append(page_content)

		#Then merge it
		document_content = "\n".join(document_content_list)
		return Content(document_content)

	def generate_document_string(self) -> str:
		'''Function to generate document using available information'''

		#Generate content and replace layout's content_string with content
		content = self.generate_content()
		document_string = self.layout.get_document_string_wth_content(content)

		return document_string


	def generate_document(self, filename: str):
		'''Function to generate document file with available information'''
		with open(filename, "w") as file:
			file.write(self.generate_document_string())

