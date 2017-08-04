import random as rdm 
from load import * 
try:
    from xtermcolor import colorize
except ImportError:
    raise ImportError('install via sudo apt install python3-xtermcolor/vivid')

quay_nb = lambda x : "RORO" if x in [2,3,4,5] else "PC"
modulo_quay = lambda x : 1 if x > 7 else x

quays  = [Quay(quay_nb(x),x) for x in range(1,7)]
cranes = [Crane(x) for x in range(7)]
cranes_queued = []
nb_crane = lambda : 2 if (rdm.random() > 0.7) else 1
verif = lambda  boat, quay : (boat.type_boat == quay.type_quay)
crisis_time = START

def sepererator() :
	try:
		print(colorize("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", ansi=36))
	except NameError:
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def compute_time(boat) :
	if boat.type_boat == "PC" : 
			nb_crane_assgn = 1
			service_time = boat.capa_cont /nb_crane_assgn
			service_time = datetime.timedelta(0,60 * service_time)
	if boat.type_boat == "RORO" : 
		manu = boat.capa_remor
		min_total = ( 40 / 60 ) *  boat.capa_cont 
		delta_assignement = max(datetime.timedelta(0,60 * min_total), datetime.timedelta(0,60 *  manu  ))
		service_time = datetime.timedelta(0,60 *  manu  )
	return service_time

def merge_quay_crane_assignement() : 
	global crisis_time
	ls_boats = read_csv(PATH)
	list_boat, list_time, list_quays, list_delays = [], [], [], []
	for boat in ls_boats : 
		service_time = compute_time(boat)
		Q = assign_quay(boat, service_time)
		C = assign_crane(boat, service_time)
		boat.starting_time = max(Q.time_freed - service_time, C.time_freed - service_time)
		boat.ending_time = max(Q.time_freed, C.time_freed)
		print("la grue sera dispo à :: " + str(C.time_freed - service_time))
		print("***") 
		print("le quai sera dispo à :: " + str(Q.time_freed - service_time))
		print("---")
		boat.ending_time = boat.departure if abs(boat.ending_time-boat.arrival_time) > abs(boat.departure-boat.arrival_time) else boat.ending_time 
		B = boat
		time = (B.arrival_time, B.ending_time)
		try : 
			print(colorize(str(B.type_boat), ansi=30)+"  :: arrive à "+colorize(str(B.arrival_time), ansi = 2)+" servi à : "+colorize(str(B.starting_time), ansi = 3)+" fini à : "+colorize(str(B.ending_time), ansi=5)+" au quai N° : "+colorize(str(Q.lib), ansi=2) + " avec un delay de :" + colorize(str(abs(B.arrival_time - B.starting_time)), ansi=95))
		except NameError : 
			"""on utilise ch pour ecrire dans le fichier log """
			print(ch = str(B.type_boat)+"  :: arrive à "+str(B.arrival_time)+" servi à : "+str(B.starting_time)+" fini à : "+str(B.ending_time)+" au quai N° : "+str(Q.lib) + " avec un delay de :" + str(abs(B.arrival_time - B.starting_time)))
		sepererator()
		list_delays.append(abs(B.arrival_time - B.starting_time))
		list_boat.append(B)
		list_time.append((B.starting_time, B.ending_time))
		list_quays.append(Q)
	return list_boat, list_time, list_quays, list_delays, crisis_time

def assign_quay(boat, service_duration) : 
	global quays 
	global cranes
	#creation de la liste des quays concernes 
	concerned = [quay for quay in quays if verif(boat, quay)]
	ls_quays_free = [quay for quay in concerned if quay.queue == False] 
	ls_quays_busy = [quay for quay in concerned if quay.queue == True] 
	#on cree une liste contenant des tuple (quay_busy, boat)
	if len(ls_quays_free) == 0 : 
		distance = []
		#print(concerned[0].type_quay)
		for busy in ls_quays_busy : 
			distance.append((abs(boat.arrival_time - busy.time_freed), busy ))
		q = min(distance, key=lambda x: x[0]) 
		q = q[1]
		q.time_freed = max(q.time_freed, boat.arrival_time)
		q.starting_time = q.time_freed 
		q.time_freed += service_duration
		q.queue = True
	else : 
		q = rdm.choice(concerned)
		q.time_freed = max(q.time_freed, boat.arrival_time)
		q.starting_time = q.time_freed
		q.time_freed +=  service_duration
		q.queue = True
		ind = quays.index(q)
		quays[ ind ] = q
		
	return q

def assign_crane(boat, service_duration): 
	"""a l'air de tres mal fonctionner !  """
	global cranes 
	global cranes_queued
	global crisis_time
	#service_time = boat.arrival_time if boat.arrival_time > c[1].time_freed else c[1].time_freed
	#if len(cranes) > 0 : 
		#print(cranes)
	#else : 
		#print(cranes_queued)
	if len(cranes) == 1: 
		crisis_time = boat.arrival_time
		print(crisis_time)
	if len(cranes) == 0 : 
		distance = [] 
		for crane in cranes_queued : 
			distance.append((abs(crane.time_freed - boat.arrival_time), crane))
		c = min(distance, key=lambda x: x[0])
		c[1].time_freed =boat.arrival_time + service_duration
		cranes_queued[cranes_queued.index(c[1])] = c[1]
		return c[1]
		#print ("la crane sera dispo à : " + str(c[1]))
	else : 
		c = cranes[0]
		del cranes[0]
		c.time_freed =boat.arrival_time + service_duration 
		c.queue = True
		cranes_queued.append(c)
		return c
	
		



if __name__ == "__main__" : 
	generate()