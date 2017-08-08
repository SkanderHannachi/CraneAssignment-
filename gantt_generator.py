from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import random
import plotly.figure_factory as ff
from core import * 

def random_color():
    levels = range(10,256,15)
    return tuple(random.choice(levels) for _ in range(3))

fast_conv = lambda x : x.strftime('%Y-%m-%d %H:%M')

def plot_gantt(sol): 
	df, ls_ress = [], []
	for elem in zip(sol.list_boat, sol.list_quays) : 
		start, end, task, ressource = elem[0].starting_time, elem[0].ending_time, elem[1].lib, elem[0].name
		start = fast_conv(start)
		end = fast_conv(end)
		ls_ress.append(ressource)
		df.append(dict(Task= task, Start=start, Finish=end, Resource=ressource))
	r, g, b = 100, 20, 50 
	colors = dict()
	for boat in ls_ress : 
		T = random_color()
		colors[boat] = 'rgb('+str(T[0])+', '+str(T[1])+', '+str(T[2])+')'
		for k in [r, g, b] : 
			k += 20
			
	#colors = dict(Cardio = 'rgb(46, 137, 205)',
				#Food = 'rgb(114, 44, 121)',
				#Sleep = 'rgb(198, 47, 105)',
				#Brain = 'rgb(58, 149, 136)',
				#Rest = 'rgb(107, 127, 135)')
	fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='Daily Schedule', show_colorbar=True, bar_width=0.4, showgrid_x=True, showgrid_y=True, group_tasks=True)
	plot(fig)
	
	
	
if __name__ == "__main__": 
	plot_gantt(generate())