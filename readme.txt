""" 

	Descriptif :
    ------------

	Resoudre le probleme d'ordonnancement avec un algo genetique : 
    
	selon l'input donne, l'algo genere des solutions acceptables mais pas forcement optimale. 
	selon les parents, il cree la population fils en se basant sur les regles de la genetique : 
				Croisement 
				Mutation 

	On definit le croisement : solution generee apartir de deux solutions parents
					Mutation : solution generee apartir d'une solution deja existante. On modifie un chromosome de la solution  
    
	La fonction fitnesse : calcule les performances de chaque epoch 
    
    
	les outils pour : 
		- Lire le csv
		- Pour generer un gantt dynamique


	Pour generer les solutions initiales : 
		On selection aleatoirement des bateaux
		On les affecte à un Quai dés la liberation de celui ci (ici ça ne sera que la seule contrainte
		On repete l'operation avec tous les bateaux
		Pour les grues, on ne peut pas raisonner sur la capacité des bateaux sinon ça entrainerait des convergences locales très rapides. On initialise randomli.
		        
    
   """
