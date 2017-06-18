import random as rdm 
from load import * 
from core import Solution


ls_boats = [] 
ls_cranes = []
ls_quays = []
ls_assignement = []

def generate() : 
    ls_boats = read_csv(PATH)
    solution = Solution(list_boat=[], list_time=[], list_cranes=[])
    #construction du tableau des quais
    while (len(ls_boats)>0) : 
        choosen = rdm.choice(ls_boats)
        del ls_boats[ls_boats.index(choosen)]
        #print(choosen.type_boat)
        #print("#################")
        
    
    
    
    
    
    
if __name__ == "__main__" : 
    generate()