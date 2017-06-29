"""                 	adam = Solution(list_boat, list_time, list_quays)
"""

import random as rdm
from load import Boat
from generate import merge_quay_crane_assignement, sepererator, crisis_time

NB_POPULATION = 10
MUTATION_CROSSOVER = 0.7   #70% chance for a mutation
PARENT_CHOICE      = 0.5

choose = lambda chance : rdm.random() < chance



def mutation(adam) : 
	"""cette fonction switch deux bateaux du même type. Il faut rajouter une condition pour que l'ecart au niveau du temps ne soit pas enorme."""
	global crisis_time
	ls_boats_to_permute = adam.list_boat
	ls_quays_to_permute = adam.list_quays
	ls_times_to_permute = adam.list_time
	crisis              = adam.crisis_time
	#print(ls_boats_to_permute)
	print(ls_times_to_permute)
	x = rdm.sample(ls_boats_to_permute, 2)
	while ( (x[0].type_boat != x[1].type_boat) and (x[0] != x[1]) ):
		x = rdm.sample(set(ls_boats_to_permute), 2) 
	gene_one = x[0]
	gene_two = x[1]
	ind_gene_boat_one = ls_boats_to_permute.index(gene_one)
	ind_gene_boat_two = ls_boats_to_permute.index(gene_two)
	gene_quay_one = ls_quays_to_permute[ind_gene_boat_one]
	gene_quay_two = ls_quays_to_permute[ind_gene_boat_two]
	gene_time_one = ls_times_to_permute[ind_gene_boat_one]
	gene_time_two = ls_times_to_permute[ind_gene_boat_two]
	first_to_arrive = min(gene_time_one[0], gene_time_two[0])
	sepererator()
	sepererator()
	sepererator()
	print("on va permuter un "+str(gene_one.type_boat)+" ; "+str(gene_one.starting_time)+" avec un "+str(gene_two.type_boat)+" ; "+str(gene_two.starting_time)+ " le premier arrive à : "+str(gene_one.arrival_time)+" et le deuxieme arrive à : "+str(gene_two.arrival_time)+"   on sera à court de crane à apartir de : "+str(adam.crisis_time))
	if  gene_one.type_boat == "PC" :
		if gene_one.arrival_time > gene_quay_two.time_freed : 
			gene_one.starting_time = gene_quay_two.time_freed
		else : 
			gene_one.starting_time = gene_one.arrival_time
		if gene_time_two > gene_quay_two.time_freed : 
			gene_two.starting_time = gene_quay_two.time_freed 
		else : 
			gene_two.starting_time = gene_two.arrival_time
		
		



class Solution : 
	"""la classe solution permet de definir une solution au probleme (ie) une solution represntable sous forme de GANTT. Elle est caracterisee par un float Performance qui nous informe sur le rendement """
	def __init__(self, list_boat, list_time, list_quays, crisis) :
		"""On la remplir avec un vecteur de bateaux et un autre vecteur sur les heures de departs et darrivee. Finalement un troisieme vecteur sur le nombre de grues. """
		self.performance = self.compute()
		self.list_boat   = list_boat                   #une liste de chaque quai accueillant chaque bateau, les quais sont numérotés
		self.list_time   = list_time                   #une liste d'une liste des temps reservés dans chaque quai pour chaque bateau
		self.list_quays  = list_quays 
		self.indiv_list  = zip(self.list_boat, self.list_time, self.list_quays) #un individu : ie la variable qui regroupe tout
		self.lenght = len(list_boat)
		self.crisis_time = crisis
        
	def compute(self) : 
		return 0

def seek_and_give_birth(ls_solution) : 
	couple = fin_besties(ls_solution)
	child  = compute_next_indiv(couple[0], couple[1])
      

def compute_next_indiv(sol_parent_1,sol_parent_2) : 
	if (choose(MUTATION_CROSSOVER)) : 
		child = crossover(sol_parent_1, sol_parent_2)
	else : 
		if (choose(PARENT_CHOICE)) : 
			child = mutation(sol_parent_1)
		else : 
			child = mutation(sol_parent_2)
	return child

	

def generate() : 
	list_boat, list_time, list_quays, crisis = merge_quay_crane_assignement()
	adam = Solution(list_boat, list_time, list_quays, crisis)
	return adam



if __name__ == "__main__" : 
	mutation(generate())
