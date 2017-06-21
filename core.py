"""                 	adam = Solution(list_boat, list_time, list_quays)
"""

import random as rdm
from load import Boat
from generate import merge_quay_crane_assignement

NB_POPULATION = 10
MUTATION_CROSSOVER = 0.7   #70% chance for a mutation
PARENT_CHOICE      = 0.5

choose = lambda chance : rdm.random() < chance



#def mutation(sol_parent_1, sol_parent_2) : 
	#x = rdm.sample(set([1, 2, 3, 4, 5, 6]), 2)


class Solution : 
	"""la classe solution permet de definir une solution au probleme (ie) une solution represntable sous forme de GANTT. Elle est caracterisee par un float Performance qui nous informe sur le rendement """
	def __init__(self, list_boat, list_time, list_quays) :
		"""On la remplir avec un vecteur de bateaux et un autre vecteur sur les heures de departs et darrivee. Finalement un troisieme vecteur sur le nombre de grues. """
		self.performance = self.compute()
		self.list_boat   = list_boat                   #une liste de chaque quai accueillant chaque bateau, les quais sont numérotés
		self.list_time   = list_time                   #une liste d'une liste des temps reservés dans chaque quai pour chaque bateau
		self.list_quays  = list_quays 
		self.indiv_list  = zip(self.list_boat, self.list_time, self.list_quays) #un individu : ie la variable qui regroupe tout
		self.lenght = len(list_boat)
        
	def compute(self) : 
		return 0

def seek_and_give_birth(ls_solution) : 
	couple = find_besties(ls_solution)
	child  = compute_next_indiv(couple[0], couple[1])
      

def compute_next_indiv(sol_parent_1,sol_parent_2) : 
	if (choose(MUTATION_CROSSOVER)) : 
		child = mutation(sol_parent_1, sol_parent_2)
	else : 
		if (choose(PARENT_CHOICE)) : 
			child = crossover(sol_parent_1)
		else : 
			child = crossover(sol_parent_2)
	return child

	

def generate() : 
	list_boat, list_time, list_quays = merge_quay_crane_assignement()
	adam = Solution(list_boat, list_time, list_quays)
	return adam



if __name__ == "__main__" : 
	generate()
