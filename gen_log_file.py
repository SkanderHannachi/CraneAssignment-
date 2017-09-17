try:
    from xtermcolor import colorize
except ImportError:
    raise ImportError('install via sudo apt install python3-xtermcolor/vivid')

def seperator_1() :
	try:
		print(colorize("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", ansi=36))
	except NameError:
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		
def seperator_2() :
	return "------------------------------------------------------------------------"


def current_thread(sol):
	for elem in zip(sol.list_boat, sol.list_quays):
		print(colorize(str(elem[0].type_boat), ansi=30)+" arrive à "+colorize(str(elem[0].arrival_time), ansi = 2)+" servi à : "+colorize(str(elem[0].starting_time), ansi = 3)+" fini à : "+colorize(str(elem[0].ending_time), ansi=5)+" au quai N° : "+colorize(str(elem[1].lib), ansi=2) + " matricule : " + str(elem[0].name))
		
		

if __name__ == "__main__": 
	current_thread(generate())
