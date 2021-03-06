from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import random
import plotly.figure_factory as ff
from core import * 


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))

fast_conv = lambda x : x.strftime('%Y-%m-%d %H:%M')

def plot_gantt(sol): 
	df, ls_ress = [], []
	T = [random_color() for _ in range(len(sol.list_boat))]
	for elem in zip(sol.list_boat, sol.list_quays) : 
		start, end, task, ressource = elem[0].starting_time, elem[0].ending_time, elem[1].lib, elem[0].name +'  ::  '+elem[0].type_boat
		start = fast_conv(start)
		end = fast_conv(end)
		ls_ress.append(ressource)
		df.append(dict(Task= task, Start=start, Finish=end, Resource=ressource))
	colors, k = dict(), 0
	for boat in ls_ress : 
		colors[boat] = 'rgb('+str(T[k][0])+', '+str(T[k][1])+', '+str(T[k][2])+')'
		k += 1
		#T = [el+15 for el in T]
		#print([elm for elm in T])
	fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='Daily Schedule', show_colorbar=True, bar_width=0.4, showgrid_x=True, showgrid_y=True, group_tasks=True)
	plot(fig)
	
	
	
if __name__ == "__main__": 
	plot_gantt(generate())
