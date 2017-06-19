"""pour liberer les grues faire un trruc du genre :
pour chercher quelle crane, on raisonne comme pour les quays : on calcule la distance la plus courte 
"""
import random as rdm 
from load import * 
from core import Solution

quay_nb = lambda x : "RORO" if x in [2,3,4,5] else "PC"
modulo_quay = lambda x : 1 if x > 7 else x

ls_boats = [] 
ls_cranes_used = []
ls_assignement = []
quays  = [Quay(quay_nb(x),x) for x in range(1,7)]
cranes = [Crane(x) for x in range(1,7)]
nb_crane = lambda : 2 if (rdm.random() > 0.7) else 1

def sepererator() :
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def find_nearest(cranes_ls, boat, number_assigned) : 
	i = 1
	distance = []
	resul = []
	for crane in cranes_ls : 
		distance.append(abs(crane.time_freed - boat.arrival_time))
	while ( 1 <= number_assigned) : 
		resul.append(min(distance))
		del cranes_ls[cranes_ls.index(crane)]
	return resul, cranes_ls 

def check_cranes_and_choose_one(boat, nb_crane_assigned) : 
	"""fonction qui voit si y'a une/des grues de libres et sinon il regarde dans la liste d'attente et choisit la grue la plus proche pour l'assigner. La fonction renvoie une liste(d'une ou de deux au max) de grues à affecter  """
	global cranes
	if len(cranes) < 1 : 
		cranes = ls_cranes_used
		crane, cranes = find_nearest(cranes, boat, nb_crane_assigned)
	else :
		crane = cranes[0:nb_crane_assigned]
		del cranes[0:nb_crane_assigned]
		try :
			crane_one = crane[0]
			crane_two = crane[1]
			crane_one = crane[0]
			crane_two = crane[1]
			crane_one.delta_freed = datetime.timedelta( ( 40 / 60 ) *  (boat.capa_cont/2) * 60 )
			crane_two.delta_freed = datetime.timedelta( ( 40 / 60 ) *  (boat.capa_cont/2) * 60 )
			crane_one.update()
			crane_two.update()
			ls_cranes_used.append(crane_one)
			ls_cranes_used.append(crane_two)
		except IndexError : 
			crane_one = crane[0]
			crane_one.delta_freed = datetime.timedelta( ( 40 / 60 ) *  (boat.capa_cont) * 60 )
			crane_one.update()
			ls_cranes_used.append(crane_one)
	return crane_one

def find_freed_time(quay, boat) :
	"""Prend en entree un objet quay et boat, et renvoie le temps de liberation (ie quand le bateau sera servi)  """
	if quay.time_freed == datetime.datetime.strptime(YEAR+'-'+MONTH+'-'+DAY+' '+'00:00','%Y-%m-%d %H:%M') : 
		quay.time_freed = boat.arrival_time 
		time = boat.arrival_time
	else : 
		if boat.arrival_time >= quay.time_freed :
			time = boat.arrival_time
			quay.time_freed = boat.arrival_time
		elif (boat.arrival_time <= quay.time_freed) :
			time = quay.time_freed
	return time

       
def assign_to_quay(boat): 
	ls_quay_lib = []
	global quays
	global cranes 
	for quay in quays : 
		"""on peut rajouter une condition pour que ce soit circulaire ET optimale """
		if (quay.type_quay == boat.type_boat) and (quay.queue == False) :
				if boat.type_boat == "PC" : 
					nb_crane_assgn = nb_crane()
					cr = check_cranes_and_choose_one(boat, nb_crane_assgn)
					min_total = boat.capa_cont /nb_crane_assgn 
					delta_assignement = datetime.timedelta(0,60 * min_total)
					# penser a ajouter delta = max(delta_assignement, delta_departure)
					quay.time_freed = boat.arrival_time  + delta_assignement
					quay.queue = True   #mais on libere quand?
					print(boat.type_boat+"  assigned to " + str(quay.lib)+"; type : "+quay.type_quay+"\n" " arrivant à  "+str(boat.arrival_time)+" termine à : " + str(quay.time_freed)+" et reste : "+str(quay.time_freed))
					sepererator()
				elif boat.type_boat == "RORO" : 
					nb_crane_assgn = 1
					manu = boat.capa_remor
					min_total = ( 40 / 60 ) *  boat.capa_cont 
					delta_assignement = max(datetime.timedelta(0,60 * min_total), datetime.timedelta(0,60 *  manu  ))
					quay.time_freed = boat.arrival_time  + delta_assignement
					quay.queue = True
					print(boat.type_boat+"  assigned to " + str(quay.lib)+"; type : "+quay.type_quay+"\n" " arrive vers  "+str(boat.arrival_time)+" termine à : " + str(quay.time_freed)+" et reste :  "+str(delta_assignement))
					sepererator()
				return quay
		elif (quay.type_quay == boat.type_boat) and (quay.queue == True) :
			for busy_quay in quays : 
				if (busy_quay.type_quay == boat.type_boat) : 
					ls_quay_lib.append((abs(busy_quay.time_freed - boat.arrival_time), busy_quay))
			quay = min(ls_quay_lib, key=lambda x: x[0])
			nb_crane_assgn = nb_crane() 
			min_total = ( 40 / 60 ) *  boat.capa_cont
			if boat.type_boat == "RORO" : 
				manu = boat.capa_remor
				min_total = max(manu, min_total)
			delta_assignement = datetime.timedelta(0,60 * min_total)
			time_service = quay[1].time_freed
			quay[1].time_freed = time_service  + delta_assignement  #not sure
			print(boat.type_boat+"  assigned to " + str(quay[1].lib)+"; type : "+quay[1].type_quay + " servi à  :"+str(time_service)+" et finit à :  "+str(quay[1].time_freed)+"  de capa :"+str(boat.capa_cont)+'\n')
			sepererator()
			return quay[1]

def generate() : 
	ls_boats = read_csv(PATH)
	solution = Solution(list_boat=[], list_time=[], list_cranes=[])
	#construction du tableau des quais
	i = 1  #pour le quai
	while (len(ls_boats)>0) : 
		i = modulo_quay(i)
		choosen_boat = rdm.choice(ls_boats)
		choosen_quay = assign_to_quay(choosen_boat)
		#find_freed_time(choosen_quay, choosen_boat)
		solution.list_boat.append(choosen_boat)
		del ls_boats[ls_boats.index(choosen_boat)]
		i += 1
	#print([elem.type_boat for elem in solution.list_boat])
	return solution 

if __name__ == "__main__" : 
	generate()