import random as rdm
from load import Boat, VesselTime
import datetime
from generate import merge_quay_crane_assignement, crisis_time
from gantt_generator import *
from gen_log_file import *


NB_POPULATION = 10
MUTATION_CROSSOVER = 0.7   #70% chance for a mutation
PARENT_CHOICE      = 0.5

choose = lambda chance : rdm.random() < chance 

def suppr(ls, l) : 
    for elem in l : 
        ls.remove(elem) 
    return ls


def delete_list_from_list(ls,l_a, l_b): 
	for elem in [l_a, l_b] : 
		ls = suppr(ls, elem)
	return ls


#def find_new_starting_time(ls_quays, ls_time, boat, service_time):
	#bl, state, k = True, False, 1
		#try : 	
			#while ((k < len(ls_time)) and ( (bl==False)) ): 
				#dis = ls_time[k].starting_time - ls_time[k-1].time_freed
				#if (boat.starting_time > ls_time[k].time_freed) and (dis + boat.starting_time < ls_time[k].starting_time) : 
					
				#elif 
				
				
				




def find_new_starting_time(ls_quays, ls_time, boat, service_time):
	bl, state, k = True, False, 1
	try : 	
		while ((k < len(ls_time)) and ( (bl==False)) ): 
			dis = ls_time[k].starting_time - ls_time[k-1].time_freed
			if dis < service_time : 
				#print("Jocker!")
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
			ls_quays[k].starting_time = boat.starting_time
			ls_quays[0].time_freed = boat.starting_time + service_time
			ls_time[0] = VesselTime(boat.starting_time, boat.ending_time, ls_quays[0].lib, ls_quays[0]) #throw ls_time
	except IndexError: 
		print("un seul quay")
	return ls_time, ls_quays, boat
		


def mutation(sol) : 
	"""Takes an instance of Solution(list_vessels, list_quays, list_times) as Input and return the mutated version.""" 
	state = True
	while(state) : 
		if choose(PARENT_CHOICE) : 
			parents = rdm.sample([2,3,4,5], 2)
		else : 
			parents = rdm.sample([1, 6], 2)  
		gene_one_ind, gene_two_ind = parents[0], parents[1]
		quay_one_ls =[elem for elem in sol.list_quays if elem.lib == gene_one_ind]
		quay_two_ls = [elem for elem in sol.list_quays if elem.lib == gene_two_ind]
		times_one_ls = [elem for elem in sol.list_time if elem.lib == gene_one_ind]
		times_two_ls = [elem for elem in sol.list_time if elem.lib == gene_two_ind]
		try : 
			boat_one_q = rdm.choice(quay_one_ls)
			boat_two_q = rdm.choice(quay_two_ls)
			state = False
		except IndexError : 
			state = True
	ind_one = sol.list_quays.index(boat_one_q)
	ind_two = sol.list_quays.index(boat_two_q)
	boat_one = sol.list_boat[ind_one]
	boat_two = sol.list_boat[ind_two]
	for q in zip(quay_one_ls, quay_two_ls) : 
		if boat_one in  q[0].vessels_in :
			print("supression..")
			q[0].vessels_in.remove(boat_one)
		if boat_two in q[1].vessels_in : 
			print("supression..")
			q[1].vessels_in.remove(boat_two)
	#updating vessels
	print(sol)
	sol.list_boat[ind_two], sol.list_boat[ind_one] = sol.list_boat[ind_one], sol.list_boat[ind_two]    
	#updating quays and times
	sol.list_quays = delete_list_from_list(sol.list_quays, quay_one_ls, quay_two_ls)
	sol.list_time = delete_list_from_list(sol.list_time, times_one_ls, times_two_ls)
	#print(times_one_ls)
	times_one_ls_modified, ls_quay_one_modified, boat_two_modified,  = find_new_starting_time(quay_one_ls, times_one_ls, boat_two, boat_two.compute_time())
	times_two_ls_modified, ls_quay_two_modified, boat_one_modified  = find_new_starting_time(quay_two_ls, times_two_ls, boat_one, boat_one.compute_time())
	sol = update(sol, times_one_ls_modified, ls_quay_one_modified, boat_two_modified, times_two_ls_modified, ls_quay_two_modified, boat_one_modified, ind_one, ind_two)
	#plot_gantt(sol)
	return sol
	
def update(sol, time_one, quay_one, boat_two, time_two, quay_two, boat_one, ind_one, ind_two):
	def add(ls, ll, l) : 
		for elem in l : 
			ls.append(elem)
		for elem in ll : 
			ls.append(elem)
		return ls
	sol.list_boat[ind_one] = boat_one
	sol.list_boat[ind_two] = boat_two
	sol.list_quays = add(sol.list_quays, quay_one, quay_two)
	sol.list_time = add(sol.list_time, time_one, time_two)
	#current_thread(sol)
	return sol
    
class Solution : 
	"""la classe solution permet de definir une solution au probleme (ie) une solution represntable sous forme de GANTT. Elle est caracterisee par un float Performance qui nous informe sur le rendement """
	def __init__(self, list_boat, list_time, list_quays, list_delays, crisis) :
		self.list_boat   = list_boat                   
		self.list_time   = list_time                   
		self.list_quays  = list_quays 
		self.list_delays = list_delays  
		self.crisis_time = crisis
		self.performance = self.compute()
	def compute(self) : 
		S = datetime.timedelta(days = 0, seconds = 0 )
		for B in self.list_boat: 
			S += abs(B.arrival_time - B.starting_time)
		return S
	def __repr__(self): #rajouter une conditon
		ch = ""
		for elem in zip(self.list_quays, self.list_boat):
			ch += "vessel de type %s, arrive a : %s au quay n° %s , commence à : %s et fini à : %s  \n" % (elem[1].type_boat, elem[1].arrival_time, elem[0].lib, elem[0].starting_time, elem[0].time_freed)
			ch += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n"
		return ch


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
	solution = generate()
	#plot_gantt(solution)
	sol = mutation(solution)

	
	
