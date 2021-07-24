from . import Tests
from . import Functional

class PageValues(Functional.Struct):
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

	def get_test(self) -> Tests.Test:
		return self.__test_option__

	def generate_test(self) -> Tests.GeneratedTest:
		'''Function to generate test option from this format'''
		return self.__test_option__.generate_test()

class PagesInformation(Functional.StructList):
	'''
	PagesInformation - class which containing information about all available pages
	Initial arguments:
	- 'structlist': list of object of PageValues class
	'''
	pass

class PageStyle:
	'''
	PageStyle - class with style information about page of document
	Inital arguments:
	- 'test_format_string': Format-type string with content of test option of the page. Must containing {excercises} element to replace them with excercises of the test, and some other text {arg1}, {arg2} from executing PageValues class, etc. Will be used in context of 'test_format_string.format(**format_arguments.dict(), excercises="Some excercises")'
	- 'excercise_format_string': Format-type string for test. Must containing {title} and {tasks} elements. Will be used in context of 'excercise_format_string.format(title="Title", tasks="Some tasks")'
	- 'tasks_format_string': Format-type string for tasks. Must containing {task} element. Will be used in context of 'tasks_format_string.format(task="This task")'
	Available attributes:
	- 'test_option_format': Page format string
	- 'excercise_format': Excercises format string
	- 'tasks_format': Tasks format string
	'''

	def __init__(self, 
			test_format_string: str, 
			excercise_format_string: str,
			tasks_format_string: str = "{task}"
	):
		self.test_option_format = test_format_string
		self.excercise_format = excercise_format_string
		self.tasks_format = tasks_format_string

	def generate_page(self, 
			format_arguments: PageValues, 
	) -> str:
		'''
		Function to generate page string from format arguments and excercises. Put all in format string and return it.
		Arguments:
		- 'format_arguments': Object of class PageValues. Containing page arguments with test option with excercises
		'''

		#Generate test for this page from available test option format of PageValues object
		generated_test = format_arguments.generate_test()

		excercises_formatted = []
		
		#For all excercises from this generated test
		for excercise in generated_test:
			
			#First of all - format all tasks of this excercise
			tasks_formatted = []

			for task in excercise:
				task_string = self.tasks_format.format(task=task.get_task())
				tasks_formatted.append(task_string)

			#Merge all tasks with new lines
			excercise_tasks = "\n".join(tasks_formatted)

			#Format excercise with title and formated tasks
			excersise_formatted = self.excercise_format.format(title=excercise.get_title(), tasks=excercise_tasks)
			
			#Add this formatted excercise in list of formatted excercises
			excercises_formatted.append(excersise_formatted)

		#Merge all excercises
		page_excercises = "\n".join(excercises_formatted)

		#Put this content inside
		page_content = self.test_option_format.format(**format_arguments.dict(), excercises=page_excercises)

		return page_content

class DocumentLayout:
	'''
	DocumentLayout - class to work with document layout information
	Initial arguments:
	- 'layout_path': Path of the document layout. This layout need to contain 'page_word' inside, will be replaced with generating page
	- 'page_style': Object of class PageStyle, which containing all information about style of the page
	- 'content_string': Word in layout file, which will be replaced with generation content. By default suppose to be "$CONTENT$"
	Available attributes:
	- 'layout': Document layout file path
	- 'pagestyle': Page style information object
	- 'contentstr': Content word in layout file
	'''
	def __init__(self, 
			layout_path: str,
			page_style: PageStyle,
			content_string: str = "#CONTENT#",
	):
		self.layout = layout_path
		self.pagestyle = page_style
		self.contentstr = content_string

	def read_layout(self) -> str:
		'''Function to read document layout'''
		layout = ""
		with open(self.layout) as file:
			layout = file.read()

		return layout

	def generate_page(self, page_value):
		return self.pagestyle.generate_page(page_value)

	def get_document_string_wth_content(self, content: str) -> str:
		'''Function to generate document with content from layout'''
		layout = self.read_layout()
		return layout.replace(self.contentstr, content)

class Document:
	'''
	Document - class to work with document using any information about it
	Inital arguments:
	- 'layout': Object of class DocumentLayout, which contains information about document layout and it's content string
	- 'pages_info': Object of class PagesInformation, which containing all information about generating page arguments and all generated tasks for this arguments
	Available attributes:
	- 'layout': Document layout object
	- 'pagesinfo': List of informations about pages, objects of PageValues class
	'''
	def __init__(self, 
			layout: DocumentLayout,
			pages_info: PagesInformation,
	):
		self.layout = layout
		self.pagesinfo = pages_info

	def generate_content(self) -> str:
		'''Function to generate pages content for document from available info'''
		
		document_content_list = []

		#For every page generate content
		for page_value in self.pagesinfo:
			
			page_content = self.layout.generate_page(page_value)
			document_content_list.append(page_content)

		#Then merge it
		document_content = "\n".join(document_content_list)
		return document_content

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

