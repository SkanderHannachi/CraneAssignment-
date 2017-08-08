import datetime
import csv 
import random

DAY  = '01' 
MONTH = '01'
YEAR  = '2017'
PATH = "bateaux.csv"
NB_CRANES = 7
START = datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DAY+' '+'00:00', '%Y-%m-%d %H:%M')

f = lambda hours : "00" if hours=="24" else hours

def read_csv(path) : 
	ls=[]
	with open(path,newline='') as csvfile : 
		boats = csv.reader(csvfile)
		for rows in boats :
			ls.append(Boat(rows[0],rows[1],rows[2],rows[3],rows[4] ))
	return sorted(ls, key=lambda x: x.arrival_time, reverse=False)

class VesselTime: 
	def __init__(self, starting_time, time_freed, lib, quay=None):
		self.starting_time = starting_time 
		self.time_freed    = time_freed
		self.lib           = lib

class Crane :
	def __init__(self, lib) : 
		self.time_freed  =  datetime.datetime.strptime(YEAR+'-'+MONTH+'-'+DAY+' '+'00:00','%Y-%m-%d %H:%M')
		self.delta_freed = datetime.timedelta(seconds = 0 )
		#self.starting_time= START
		self.lib = lib
	def __gt__(self, autre): 
		return self.time_freed > autre.time_freed 

class Quay : 
	def __init__(self, type_quay, lib): 
		self.type_quay      = type_quay 
		self.time_freed = datetime.datetime.strptime(YEAR+'-'+MONTH+'-'+DAY+' '+'00:00','%Y-%m-%d %H:%M')         # de type time
		self.starting_time = START
		self.lib = lib
		self.queue= False
		self.vessels_in=[]
	def __gt__(self, autre): 
		return self.time_freed > autre.time_freed
class Boat : 
	def __init__ (self,type_boat,arrival,departure,capa_cont,capa_remor) : 
		self.type_boat = type_boat 
		self.arrival_time  = self.convert_time(arrival) 
		self.departure     = self.convert_time(departure)
		self.starting_time = START
		self.ending_time   = START
		self.capa_cont     = int(capa_cont)
		self.capa_remor    = int(capa_remor) if capa_remor != '-' else 0
		self.is_departure  = True if (departure[0]=="D") else False     #nous informe si le bateau possede un fenetrage ou pas
		self.name          = self.name_generator()
	def compute_time(self) :
		if self.type_boat == "PC" : 
				nb_crane_assgn = 1
				service_time = self.capa_cont /nb_crane_assgn
				service_time = datetime.timedelta(0,60 * service_time)
		if self.type_boat == "RORO" : 
			manu = self.capa_remor
			min_total = ( 40 / 60 ) *  self.capa_cont 
			delta_assignement = max(datetime.timedelta(0,60 * min_total), datetime.timedelta(0,60 *  manu  ))
			service_time = datetime.timedelta(0,60 *  manu  )
		return service_time
	
	def name_generator(self): 
		namealpha = random.sample(set([chr(i) for i in range(65, 91)]), 4)
		id_alpha  = random.randint(10,99)
		ch= ""
		for elem in namealpha : 
			ch += elem 
		ch += str(id_alpha)
		return ch

	def convert_time(self, ch) : 
		if ch == "-" : 
			return START
		elif ch[0]=="D" : 
			return datetime.datetime.strptime(YEAR+'-'+MONTH+'-'+str(int(DAY)+1)+' '+f(ch[2:4])+':'+ch[5:7], '%Y-%m-%d %H:%M')
		else : 
			return datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DAY+' '+f(ch[:2])+':'+ch[3:5], '%Y-%m-%d %H:%M')
   

def main() : 
	read_csv(PATH)


if __name__ == "__main__" : 
	main()
