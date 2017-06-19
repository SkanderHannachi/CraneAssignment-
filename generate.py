import random as rdm 
from load import * 
from core import Solution

quay_nb = lambda x : "RORO" if x in [2,3,4,5] else "PC"
modulo_quay = lambda x : 1 if x > 7 else x

ls_boats = [] 
ls_cranes = []
ls_assignement = []
quays = [Quay(quay_nb(x),x) for x in range(1,7)]
nb_crane = lambda : 2 if (rdm.random() > 0.7) else 1

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
                    crane = nb_crane() 
                    min_total = boat.capa_cont /crane 
                    delta_assignement = datetime.timedelta(0,60 * min_total)
                    # penser a ajouter delta = max(delta_assignement, delta_departure)
                    quay.time_freed = boat.arrival_time  + delta_assignement
                quay.queue = True   #mais on libere quand?
                print(boat.type_boat+"  assigned to " + str(quay.lib)+"; type : "+quay.type_quay+"\n" " arrivant à  "+str(boat.arrival_time)+" et fini à : " + str(quay.time_freed))
                return quay
        elif (quay.type_quay == boat.type_boat) and (quay.queue == True) :
            for busy_quay in quays : 
                if (busy_quay.type_quay == boat.type_boat) : 
                    ls_quay_lib.append((abs(busy_quay.time_freed - boat.arrival_time), busy_quay))
            quay = min(ls_quay_lib, key=lambda x: x[0])
            crane = nb_crane() 
            min_total = boat.capa_cont / crane
            delta_assignement = datetime.timedelta(0,60 * min_total)
            quay[1].time_freed = boat.arrival_time  + delta_assignement  #not sure
            print(boat.type_boat+"  assigned to " + str(quay[1].lib)+"; type : "+quay[1].type_quay + " à :"+str(quay[1].time_freed)+" et finit à :  "+str(quay[1].time_freed)+"  de capa :"+str(boat.capa_cont)+'\n')
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
        
        
    print([elem.type_boat for elem in solution.list_boat])
    return solution 
        
        
    
    
    
    
    
    
if __name__ == "__main__" : 
    generate()