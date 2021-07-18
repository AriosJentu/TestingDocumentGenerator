from . import Variant

class PageArguments:
	'''
	PageArguments - class with Struct format, working with dictionaries.
	Initial arguments:
	- 'variant': Generated variant for this page (object of class GeneratedVariant) 
	- 'entries': Dictionary of values, which will be used in generation
	'''

	def __init__(self, 
			variant: Variant.GeneratedVariant, 
			**entries
	):
		self.__variant__ = variant
		self.__dict__.update(entries)
		self.__keys__ = entries.keys()

	def get_variant(self) -> Variant.GeneratedVariant:
		return self.__variant__

	def __iter__(self):
		for i in self.__keys__:
			yield self.__dict__.get(i)

	def __len__(self):
		return len(self.__keys__)

	def __getitem__(self, item):
		return self.__dict__.get(item)

	def dict(self):
		return {key: self.__dict__.get(key) for key in self.__keys__}

class PageStyle:
	'''
	PageStyle - class with style information about page of document
	Inital arguments:
	- 'variant_format_string': Format-type string with content of variant of the page. Must containing {excercises} element to replace them with excercises of the variant, and some other text {arg1}, {arg2} from executing PageArguments class, etc. Will be used in context of 'page_format_string.format(**format_arguments.dict(), excercises="Some excercises")'
	- 'excercise_format_string': Format-type string for variant. Must containing {title} and {tasks} elements. Will be used in context of 'excercise_format_string.format(title="Title", tasks="Some tasks")'
	- 'tasks_format_string': Format-type string for tasks. Must containing {task} element. Will be used in context of 'tasks_format_string.format(task="This task")'
	Available attributes:
	- 'variant_format': Page format string
	- 'excercise_format': Excercises format string
	- 'tasks_format': Tasks format string
	'''

	def __init__(self, 
			variant_format_string: str, 
			excercise_format_string: str,
			tasks_format_string: str = "{task}"
	):
		self.variant_format = variant_format_string
		self.excercise_format = excercise_format_string
		self.tasks_format = tasks_format_string

	def generate_page(self, 
			format_arguments: PageArguments, 
	) -> str:
		'''
		Function to generate page string from format arguments and excercises. Put all in format string and return it.
		Arguments:
		- 'format_arguments': Object of class PageArguments. Containing page arguments with variant with excercises
		'''

		excercises_formatted = []
		#For all excercises from variant
		for excercise in format_arguments.get_variant():
			
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
		page_content = self.variant_format.format(**format_arguments.dict(), excercises=page_excercises)

		return page_content

class Document:
	'''
	Document - class to work with document using any information about it
	Inital arguments:
	- 'layout_path': Path of the document layout. This layout need to contain 'page_word' inside, will be replaced with generating page
	- 'page_style': Object of class PageStyle, which containing all information about style of the page
	- 'pages_info': List of objects of class PageArguments, which containing all information about generating page arguments and all generated tasks for this arguments
	- 'content_string': Word in layout file, which will be replaced with generation content. By default suppose to be "$CONTENT$"
	Available attributes:
	- 'layout': Document layout file path
	- 'pagestyle': Page style information object
	- 'pagesinfo': List of informations about pages, objects of PageArguments class
	- 'contentstr': Content word in layout file
	'''
	def __init__(self, 
			layout_path: str,
			page_style: PageStyle,
			pages_info: list[PageArguments],
			content_string: str = "$CONTENT$",
	):
		self.layout = layout_path
		self.pagestyle = page_style
		self.pagesinfo = pages_info
		self.contentstr = content_string

	def generate_content(self) -> str:
		'''Function to generate pages content for document from available info'''
		
		document_content_list = []

		#For every page generate content
		for pageargument in self.pagesinfo:
			
			page_content = self.pagestyle.generate_page(pageargument)
			document_content_list.append(page_content)

		#Then merge it
		document_content = "\n".join(document_content_list)
		return document_content

	def generate_document_string(self) -> str:
		'''Function to generate document using available information'''

		#Open layout document to read layout:
		with open(self.layout) as file:
			layout_string = file.read()

		#Generate content and replace layout's content_string with content
		content = self.generate_content()
		document = layout_string.replace(self.contentstr, content)

		return document

	def generate_document(self, filename: str):
		'''Function to generate document file with available information'''
		with open(filename, "w") as file:
			file.write(self.generate_document_string())

