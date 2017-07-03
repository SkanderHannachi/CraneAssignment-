

	Descriptif :
        ------------

	Resoudre le probleme d'ordonnancement avec un algo genetique : 
    
	selon l'input donne, l'algo genere des solutions acceptables mais pas forcement optimales. 
	selon les parents, il cree la population fils en se basant sur les regles de la genetique : 
				Croisement 
				Mutation 

	On definit le croisement : solution generee apartir de deux solutions parents
		    la  Mutation : solution generee apartir d'une solution deja existante. On modifie un chromosome de la solution  
    
	La fonction fitnesse : calcule les performances de chaque epoch 
    
    
	les outils pour : 
		- Lire le csv
		- Pour generer un gantt dynamique


	Pour generer les solutions initiales : 
		On selection aleatoirement des bateaux
		On les affecte à un Quai dés la liberation de celui ci (ici ça ne sera que la seule contrainte, car on attend egalement la liberation de la grue.
		On repete l'operation avec tous les bateaux
	
		        
    
   
