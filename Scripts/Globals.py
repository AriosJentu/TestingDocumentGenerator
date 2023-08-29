def Initialize():
	global CurrentModule, CurrentConfiguration, AvailableLogging
	CurrentModule = None
	CurrentConfiguration = None
	AvailableLogging = {
		"logging": False,
		"show_errors": True,
		"with_time": False,
		"simple": True,
		"call": print,
	}