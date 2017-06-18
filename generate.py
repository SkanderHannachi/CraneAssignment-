import random as rdm 
from load import * 
from core import Solution

quay_nb = lambda x : "RORO" if x in [2,3,4,5] else "PC"
modulo_quay = lambda x : 1 if x > 7 else x

ls_boats = [] 
ls_cranes = []
ls_assignement = []
quays = [Quay(quay_nb(x),x) for x in range(1,7)]

def find_freed_time(quay, boat) :
    """Prend en entree un objet quay et boat, et renvoie le temps de liberation (ie quand le bateau sera servi)  """
    if boat.arrival_time > quay.time_freed :
        time = boat.arrival_time
        quay.time_freed = boat.arrival_time
    elif boat.arrival_time <= quay.time_freed
        time = quay.time_freed
    return time
        
def assign_to_quay(boat): 
    for quay in quays : 
        """on peut rajouter une condition pour que ce soit circulaire ET optimale """
        if quay.type_quay == boat.type_boat : 
            return quay.lib
            #print(boat.type_boat+"  assigned to " + quay.lib+"; type : "+quay.type_quay)
        else : 
            pass


def generate() : 
    ls_boats = read_csv(PATH)
    solution = Solution(list_boat=[], list_time=[], list_cranes=[])
    #construction du tableau des quais
    i = 1  #pour le quai
    while (len(ls_boats)>0) : 
        i = modulo_quay(i)
        choosen_boat = rdm.choice(ls_boats)
        solution.list_boat.append(choosen_boat)
        del ls_boats[ls_boats.index(choosen_boat)]
        
        i += 1
        
        
    print([elem.type_boat for elem in solution.list_boat])
    return solution 
        
        
    
    
    
    
    
    
if __name__ == "__main__" : 
    generate()