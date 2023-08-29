import datetime

from Scripts import Globals

class Logging:
	'''
		Class for working with logging inside any project. Can generate any log information and show it if it needs to be shown.
		Has a parameters:
		- logging (default: False): hide/show log information in runtime
		- show_errors (default: True): hide/show log information about errors in runtime
		- with_time (default: False): hide/show timestamp in log
		- simple (default: True): show simple timestamp in logd
		- call (default: print): function to use in logging to print information
	'''

	logging = Globals.AvailableLogging["logging"]
	show_errors = Globals.AvailableLogging["show_errors"]
	with_time = Globals.AvailableLogging["with_time"]
	simple = Globals.AvailableLogging["simple"]
	call = Globals.AvailableLogging["call"]

	@staticmethod
	def __time_format__() -> str:
		if Logging.with_time:
			if Logging.simple:
				return f"({str(datetime.datetime.today().strftime('%d/%m/%y %H:%M:%S'))})"
			return f"({str(datetime.datetime.now())})"
		else:
			return ""

	@staticmethod
	def log(*args, **kwargs):
		if Logging.logging:
			if Logging.with_time:
				return Logging.call(
					Logging.__time_format__(), 
					*args, **kwargs
				)
			else:
				return Logging.call(
					*args, **kwargs
				)

	@staticmethod
	def logpref(*args, prefix: str = "", **kwargs):
		if Logging.logging:
			if Logging.with_time:
				return Logging.__log_prefix__(prefix,
					Logging.__time_format__(), 
					*args, **kwargs
				)
			else:
				return Logging.__log_prefix__(prefix,
					*args, **kwargs
				)

	@staticmethod
	def __log_prefix__(prefix, *args, **kwargs):
		if Logging.logging:
			if Logging.with_time:
				return Logging.call(
					prefix,
					Logging.__time_format__(), 
					*args, **kwargs
				)
			else:
				return Logging.call(
					prefix,
					*args, **kwargs
				)

	@staticmethod
	def info(*args, **kwargs):
		if Logging.logging:
			return Logging.__log_prefix__(
				"[INFO]:", 
				*args, **kwargs
			)

	@staticmethod
	def warning(*args, **kwargs):
		if Logging.logging:
			return Logging.__log_prefix__(
				"[WARN]:", 
				*args, **kwargs
			)
	
	@staticmethod
	def error(*args, **kwargs):
		if Logging.logging or Logging.show_errors:
			return Logging.__log_prefix__(
				"[ERRR]:", 
				*args, **kwargs
			)

	@staticmethod
	def newline():
		if Logging.logging:
			return Logging.call("")
