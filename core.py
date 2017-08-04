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

def pick_up(PA, PB) : 
	x = rdm.choice(PA.list_boat)
	y = rdm.choice(PB.list_boat)
	while (x == y) or (x.type_boat != y.type_boat) : 
		y = rdm.choice(PB.list_boat)
	return x,y 

def update(new_boat, quay) : 
	new_boat.starting_time = max(new_boat.arrival_time, quay.starting_time)
	new_boat.ending_time   = new_boat.starting_time 
	return new_boat

def crossover(PA, PB) : 
	"""prends deux solutions en entrée. """
	gene_one, gene_two = pick_up(PA, PB) 
	ind_A = PA.list_boat.index(gene_one)
	ind_B = PB.list_boat.index(gene_two)
	gene_quay_one = PA.list_quays[ind_A]
	gene_quay_two = PA.list_quays[ind_B]
	service_time_A = compute_time(gene_one)
	service_time_B = compute_time(gene_two)
	# dans ce qui suit, les quays ne "bougent" pas contrairement aux boats
	gene_quay_one.starting_time = max(gene_two.arrival_time, gene_quay_one.starting_time)
	gene_quay_two.starting_time = max(gene_one.arrival_time, gene_quay_two.starting_time)
	gene_quay_one.time_freed += service_time_B
	gene_quay_two.time_freed += service_time_A
	PA.list_boat[ind_A] = update(gene_one, gene_quay_two)
	PB.list_boat[ind_B] = update(gene_two, gene_quay_one)
	PA.list_quays[ind_A] = gene_quay_one
	PB.list_quays[ind_A] = gene_quay_two
	return PA if max(PA.performance, PB.performance) == PA.performance else PB
	

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
	#mutated = mutation(sol)
	#print(mutated.list_boat == sol.list_boat)
	#for elem in mutated.list_boat
	#print(mutated.list_boat)
	sepererator()
	#for i in range(50000) : 
		#sol = crossover(sol, sol)
		#print(sol.performance)
	
	