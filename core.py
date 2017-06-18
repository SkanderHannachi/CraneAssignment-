"""    def __gt__(self, autre): #>+
        return self.liberation > autre.liberation     """

import random as rdm
from load import Boat

NB_POPULATION = 10
MUTATION_CROSSOVER = 0.7   #70% chance for a mutation
PARENT_CHOICE      = 0.5

choose = lambda chance : rdm.random() < chance


class Solution : 
    """la classe solution permet de definir une solution au probleme (ie) une solution represntable sous forme de GANTT. Elle est caracterisee par un float Performance qui nous informe sur le rendement """
    def __init__(self, list_boat, list_time, list_cranes) :
        """On la remplir avec un vecteur de bateaux et un autre vecteur sur les heures de departs et darrivee. Finalement un troisieme vecteur sur le nombre de grues. """
        self.performance = self.compute()
        self.list_boat   = list_boat                           #ie une liste d'objet Boat qu'on aura à remplir et à mettre à jour 
        self.list_time   = list_time 
        self.list_cranes = list_cranes
        self.indiv_list  = zip(self.list_boat, self.list_time, self.list_cranes)
        
    def compute(self) : 
        return 0

#def find_besties() :
    
  
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

def core() : 
    return 0



if __name__ == "__main__" : 
    core()
