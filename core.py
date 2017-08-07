"""PA et PB sont deux parents (deux solutions). La mutaion est le cas particulier 
	mutation(adam) == crossover(adam, adam) la mutation est la forme quadratique associée à la la forme bilinéaire symétrique de la fnc crossover. 

Une idee : raisonner sur le delay time pour améliorer les perfo à chaque epoch, ie : chercher ceux succebtibles de se permuter et possédant un delay time > 0 

"""

import random as rdm
from load import Boat
import datetime
from generate import merge_quay_crane_assignement, sepererator, crisis_time, compute_time


NB_POPULATION = 10
MUTATION_CROSSOVER = 0.7   #70% chance for a mutation
PARENT_CHOICE      = 0.5

choose = lambda chance : rdm.random() < chance 

def suppr(ls, l) : 
    for elem in l : 
        ls.remove(elem) 
    return ls

def pick_up(soluion) : 
	x = rdm.choice(PA.list_boat)
	y = rdm.choice(PB.list_boat)
	while (x == y) : 
		y = rdm.choice(PB.list_boat)
	return x,y 
    

def update(new_boat, quay) : 
	new_boat.starting_time = max(new_boat.arrival_time, quay.starting_time)
	new_boat.ending_time   = new_boat.starting_time 
	return new_boat

def extract(PA, ind) : 
    return [elem for elem in PA.list_quays if elem == ind]

#def insert_and_update(solution, ls_quay_modified, boat_to_inster): 
    #if boat_to_inster.arrival_time < 

def find_new_starting_time(ls_quays, ls_time, boat, service_time):
	bl, state, k = True, False, 1
	while ((k <= len(ls_time)) or (bl==True) ): 
		dis = ls_time[k].time_freed - ls_time[k-1].starting_time
		if dis < service_time : 
			print("bing!")
			bl = False
			state = True
		else : 
			state = False
			k += 1
	if ( boat.arrival_time + service_time < ls_time[0].starting_time ) and (state == False): 
		boat.starting_time = boat.arrival_time 
		boat.ending_time  = boat.starting_time + service_time 
		ls_quays[0].starting_time = boat.starting_time
		ls_quays[0].time_freed = boat.starting_time + service_time
		ls_time[0] = VesselTime(boat.starting_time, boat.ending_time, ls_quays[0].lib, ls_quays[0]) #throw ls_time
	elif (state == False) : 
		boat.starting_time = ls_time[-1].time_freed 
		boat.ending_time  = boat.starting_time + service_time 
		ls_quays[-1].starting_time = boat.starting_time
		ls_quays[-1].time_freed = boat.starting_time + service_time
		ls_time[-1] = VesselTime(boat.starting_time, boat.ending_time, ls_quays[-1].lib, ls_quays[-1]) #throw ls_time
	elif (state == True) : 
		boat.starting_time = boat.arrival_time 
		boat.ending_time  = boat.starting_time + service_time 
		ls_quays[0].starting_time = boat.starting_time
		ls_quays[0].time_freed = boat.starting_time + service_time
		ls_time[0] = VesselTime(boat.starting_time, boat.ending_time, ls_quays[0].lib, ls_quays[0]) #throw ls_time
		
		
		
	
	
	


def mutation(sol) : 
	"""Prends une solution et pick deux quays aléatoirement """ 
	state = True
	while(state) : 
		if choose(PARENT_CHOICE) : 
			parents = rdm.sample([2,3,4,5], 2)
		else : 
			parents = rdm.sample([1, 6], 2)  #bof
		gene_one_ind, gene_two_ind = parents[0], parents[1]
		print(gene_one_ind)
		print(gene_two_ind)
		print("######")
		for quay in sol.list_quays : 
			print(quay.time_freed)
		quay_one_ls =[elem for elem in sol.list_quays if elem.lib == gene_one_ind]
		quay_two_ls = [elem for elem in sol.list_quays if elem.lib == gene_two_ind]
		times_one_ls = [elem for elem in sol.list_time if elem.lib == gene_one_ind]
		times_two_ls = [elem for elem in sol.list_time if elem.lib == gene_two_ind]
		print(quay_one_ls) #c est ces lists quon va manipuler
		print(quay_two_ls)
		try : 
			boat_one_q = rdm.choice(quay_one_ls)
			boat_two_q = rdm.choice(quay_two_ls)
			state = False
		except IndexError : 
			state = True
	boat_one = sol.list_boat[sol.list_quays.index(boat_one_q)]
	boat_two = sol.list_boat[sol.list_quays.index(boat_two_q)]
	print(" Boat_1 :  "  +str(boat_one.arrival_time))
	print(" Boat_2 :  "  +str(boat_two.arrival_time))
	for elem in [quay_one_ls, quay_two_ls] : 
		l = suppr(sol.list_quays, elem)
	for elem in times_one_ls : 
		print("de "+str(elem.starting_time)+" a "+str(elem.time_freed))
	times_one_ls_modified = find_new_starting_time(times_one_ls, boat_two)
	times_two_ls_modified = find_new_starting_time(times_two_ls, boat_one)
    
    
class Solution : 
	"""la classe solution permet de definir une solution au probleme (ie) une solution represntable sous forme de GANTT. Elle est caracterisee par un float Performance qui nous informe sur le rendement """
	def __init__(self, list_boat, list_time, list_quays, list_delays, crisis) :
		"""On la remplir avec un vecteur de bateaux et un autre vecteur sur les heures de departs et darrivee. Finalement un troisieme vecteur sur le nombre de grues. """
		self.list_boat   = list_boat                   
		self.list_time   = list_time                   
		self.list_quays  = list_quays 
		self.list_delays = list_delays    # on aura besoin de calculer le tempsd'attente entre l'arrivee et le depart pour computer les perfs 
		self.lenght = len(list_boat)
		self.crisis_time = crisis
		self.performance = self.compute()
	def compute(self) : 
		S = datetime.timedelta(seconds = 0 )
		for elem in self.list_delays : 
			 S += elem 
		return S

def seek_and_give_birth(ls_solution) : 
	couple = find_besties(ls_solution)
	child  = compute_next_indiv(couple[0], couple[1])
      
def compute_next_indiv(sol_parent_1,sol_parent_2) : 
	if (choose(MUTATION_CROSSOVER)) : 
		child = crossover(sol_parent_1, sol_parent_2)
	else : 
		if (choose(PARENT_CHOICE)) : 
			child = crossover(sol_parent_1, sol_parent_1)
		else : 
			child = crossover(sol_parent_2, sol_parent_2)
	return child

def generate() : 
	list_boat, list_time, list_quays, list_delays, crisis = merge_quay_crane_assignement()
	adam = Solution(list_boat, list_time, list_quays, list_delays, crisis)
	return adam

if __name__ == "__main__" : 
	sol = generate()
	mutation(sol)
	#mutated = mutation(sol)
	#print(mutated.list_boat == sol.list_boat)
	#print(mutated.list_boat)
	#sepererator()
	##for i in range(50000) : 
    #crossover(sol, sol)
		#print(sol.performance)
	
	
