import random as rdm 
from load import * 


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


def merge_quay_crane_assignement() : 
	global crisis_time
	ls_boats = read_csv(PATH)
	list_boat, list_time, list_quays, list_delays = [], [], [], []
	for boat in ls_boats : 
		#Q = Quay()
		service_time = boat.compute_time()
		Q = assign_quay(boat, service_time)
		#print("quai se libère a : " + str(Q.time_freed))
		#print(Q.time_freed)
		C = assign_crane(boat, service_time)
		boat.starting_time = max(Q.time_freed - service_time, C.time_freed - service_time)
		boat.ending_time = max(Q.time_freed, C.time_freed)
		boat.ending_time = boat.departure if abs(boat.ending_time-boat.arrival_time) > abs(boat.departure-boat.arrival_time) else boat.ending_time 
		B = boat
		time = (B.arrival_time, B.ending_time)
		sepererator()
		Q.time_freed = B.ending_time
		#Q.starting_time = B.ending_time
		V = VesselTime(B.starting_time, B.ending_time, Q.lib, Q)
		list_delays.append(abs(B.arrival_time - B.starting_time))
		list_boat.append(B)
		list_time.append(V)
		list_quays.append(Q)
		#print("quai se libère a : " + str(Q.time_freed))
	#for quay in list_quays : 
		#print(str(quay.starting_time)+"  fini aa  ::  "+str(quay.time_freed)+" quai n° : " +str(quay.lib) )
	for times in list_time : 
		print(str(times.starting_time) + "  fini a "+str(times.time_freed)+"  au quai n : "+str(times.lib) )
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
		#if service_duration + boat.arrival_time > q.ti
		q = min(distance, key=lambda x: x[0]) 
		q = q[1]  #quay busy
		indc = ls_quays_busy.index(q)
		ind = quays.index(q)
		q.starting_time = max(q.time_freed, boat.arrival_time) 
		q.time_freed = q.starting_time + service_duration
		q.queue = True
		q.vessels_in.append(boat)
		#ls_quays_busy[indc] = q 
		quays[ ind ] = q
	else : 
		q = rdm.choice(ls_quays_free)
		q.starting_time = max(q.time_freed, boat.arrival_time)
		q.time_freed = q.starting_time + service_duration
		q.queue = True
		q.vessels_in.append(boat)
		ind = quays.index(q)
		quays[ ind ] = q
	#print("quai se libère a : " + str(q.time_freed))
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
	affich()
