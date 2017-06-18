"""Pour le plotting penser a faire un gantt dynamique qui change pour change pour chaque solution """

import datetime
import csv 

DAY  = '01' 
MONTH = '01'
YEAR  = '2017'
PATH = "/home/skndr-ros/salah_stage/bateaux.csv"
NB_CRANES = 7

f = lambda hours : "00" if hours=="24" else hours

def read_csv(path) : 
    ls=[]
    with open(path,newline='') as csvfile : 
        boats = csv.reader(csvfile)
        for rows in boats :
            ls.append(Boat(rows[0],rows[1],rows[2],rows[3],rows[4] ))
        #for elem in ls : 
            #print(elem.departure)
            #print("  possede un fenetrage ? : "+ str(elem.is_departure))
    return ls

class Crane :
    """La classe grue. Elle contient l'information sur le nombre de gruess 
    affectees """
    def __init__(self) : 
        self.to_last = to_last       #combien de grues restantes
        self.ls_boats = ls_boats 
        self.ls_quays = ls_quays 
    
    def update(self, assigned) : 
        self.to_last -= assigned

class Quay : 
    def __init__(self, type_quay, lib, crane_assigned = None, time_freed = None): 
        self.type_quay      = type_quay 
        self.crane_assigned = crane_assigned     # si une grue ou plus est assignee 
        self.time_freed = time_freed         # de type time
        self.lib = lib
        
    
class Boat : 
    def __init__ (self,type_boat,arrival,departure,capa_cont,capa_remor) : 
        self.type_boat = type_boat 
        self.arrival_time = self.convert_time(arrival) 
        self.departure    = self.convert_time(departure)
        self.capa_cont    = capa_cont
        self.capa_remor   = capa_remor
        self.is_departure = True if (departure[0]=="D") else False     #nous informe si le bateau possede un fenetrage ou pas
        
    def convert_time(self, ch) : 
        if ch == "-" : 
            return datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DAY+' '+'00:00', '%Y-%m-%d %H:%M')
        elif ch[0]=="D" : 
            return datetime.datetime.strptime(YEAR+'-'+MONTH+'-'+str(int(DAY)+1)+' '+f(ch[2:4])+':'+ch[5:7], '%Y-%m-%d %H:%M')
        else : 
            return datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DAY+' '+f(ch[:2])+':'+ch[3:5], '%Y-%m-%d %H:%M')
    
   

def main() : 
    read_csv(PATH)


if __name__ == "__main__" : 
    main()
