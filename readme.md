

# Objectif :
      
Resoudre le probleme d'ordonnancement avec un algo genetique : 
    
selon les données passées en entrée, l'algorithme une première solution acceptable mais pas forcément optimale. 
Des parents sont alors générés par mutation de la solution originale. La population fille est créee en se basant sur les règles de la génétique.
	* Croisement (Solution_1, Solution_2) 
	* Mutation (Solution) 

La fonction fitnesse : calcule les performances de chaque epoch 
    
### Prerequisites

* xtermcolor
* plotly

Pour generer les solutions initiales : 
	* On selection aleatoirement des bateaux
	* On les affecte à un Quai dés la liberation de celui ci (ici ça ne sera que la seule contrainte, car on attend egalement la liberation de la grue.
	* On repete l'operation avec tous les bateaux
	

