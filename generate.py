"""pour liberer les grues faire un trruc du genre :
pour chercher quelle crane, on raisonne comme pour les quays : on calcule la distance la plus courte 

ls_cranes_used.append(crane)
	for i in range(1,crane_nb) : 
		del cranes[crane] 
		if len(ls_cranes_used) => 7 : 
			cranes  = ls_cranes_used 
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


def find_nearest(cranes_ls, boat) : 
	distance = []
	for crane in zip(cranes_ls) : 
		distance.append(abs(crane.time_freed - boat.arrival_time))
	crane = min(distance)
	del cranes_ls[cranes_ls.index(crane)]
	return [crane], cranes_ls 

def check_cranes_and_choose_one(boat, nb_crane_assigned) : 
	if len(cranes) < 1 : 
		cranes = ls_cranes_used
		crane, cranes = find_nearest(cranes, boat)
	else :
		crane = [cranes[0:nb_crane_assigned]]
		del cranes[0:nb_crane_assigned]
		try : 
			crane[0].delta_freed = datetime.timedelta( ( 40 / 60 ) *  (boat.capa_cont/2) * 60 )
			crane[1].delta_freed = datetime.timedelta( ( 40 / 60 ) *  (boat.capa_cont/2) * 60 )
			crane[0].update()
			crane[1].update()
			ls_cranes_used.append(crane[0])
			ls_cranes_used.append(crane[1])
			
		except IndexError : 
			crane[0].delta_freed = datetime.timedelta( ( 40 / 60 ) *  (boat.capa_cont) * 60 )
			crane[0].update()
			ls_cranes_used.append(crane[0])
	return crane[0]
			

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
	for quay in quays : 
		"""on peut rajouter une condition pour que ce soit circulaire ET optimale """
		if (quay.type_quay == boat.type_boat) and (quay.queue == False) :
				if boat.type_boat == "PC" : 
					nb_crane_assgn = nb_crane()
					check_cranes_and_choose_one(boat, nb_crane_assgn)
					min_total = boat.capa_cont /nb_crane_assgn 
					delta_assignement = datetime.timedelta(0,60 * min_total)
					# penser a ajouter delta = max(delta_assignement, delta_departure)
					quay.time_freed = boat.arrival_time  + delta_assignement
				quay.queue = True   #mais on libere quand?
				print(boat.type_boat+"  assigned to " + str(quay.lib)+"; type : "+quay.type_quay+"\n" " arrivant à  "+str(boat.arrival_time)+" et fini à : " + str(quay.time_freed)+" il reste : "+str(quay.time_freed))
				if boat.type_boat == "RORO" : 
					nb_crane_assgn = 1
					manu = boat.capa_remor
					min_total = ( 40 / 60 ) *  boat.capa_cont 
					#delta_assignement = max(datetime.timedelta(0,60 * min_total), datetime.timedelta(0,60 * ( (manu // 60)*60 + ( manu % 60 ) ) ))
					delta_assignement = max(datetime.timedelta(0,60 * min_total), datetime.timedelta(0,60 *  manu  ))
					quay.time_freed = boat.arrival_time  + delta_assignement
					print(boat.type_boat+"  assigned to " + str(quay.lib)+"; type : "+quay.type_quay+"\n" " arrive vers  "+str(boat.arrival_time)+" et fini à : " + str(quay.time_freed)+" et reste :  "+str(delta_assignement))
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
			quay[1].time_freed = boat.arrival_time  + delta_assignement  #not sure
			print(boat.type_boat+"  assigned to " + str(quay[1].lib)+"; type : "+quay[1].type_quay + " à :"+str(boat.arrival_time)+" et finit à :  "+str(quay[1].time_freed)+"  de capa :"+str(boat.capa_cont)+'\n')
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