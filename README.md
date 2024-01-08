# Setup
Nous allons utiliser le package [screen](https://wiki.debian.org/fr/Screen) qui nous permettra de séparer le terminal pour la station et le site, ce qui permettra aussi de pouvoir fermer les terminaux sans pour autant faire stopper la prise de données.  
`sudo apt install screen`  
Nous allons désormais créer un screen pour faire tourner le site  
`screen -S site`  
On se connecte à l'aide de la commande  
`screen -x site`  
Maintenant, nous pouvons démarrer le site.  
`python3 start1.py`  
Pour quitter le screen, nous utilisons le raccourci  
`Ctrl+A+D`  
On réitère le même processus pour la station  
`screen -S station`   
`screen -x station`  
Puis enfin,  
`python3 start2.py`

# Contenu des fichiers de code :

### Site :
	
	graphique.js :
	    	Contient le code nécessaire à la création des graphiques ainsi que le changement du graphique sélectionné en appuyant sur les boutons.
	
	global.js :
	    	Contient le code utile à plusieurs pages : flèches pour naviguer à l'élément précédent / suivant, la fonction de recherche, le bouton "Aujourd'hui" et les mois et 		jours 	des calendriers qui ouvrent l'élément correspondant.
	
	index.py :
		Contient le code pour héberger le site et l'adaptabilité des pages en fonction des données.
	
	
### Raspberry : 
	
	debug.py : 
	 	Permet de visualiser les données en temps réel, permet aussi de déboguer en affichant les potentiels erreurs des capteurs.
	capteurs.py :
	     	Fichier indispensable qui permet de récupérer les données des capteurs.
	init.py : 
	 	Fichier qui doit être lancé lorsque l'on veut démarrer la station. (Automatiquement démarré par start2.py)
	station.py : 
	    	Permet de lancer la station, ne pas utiliser ce fichier lors de la première initialisation
### Global : 
	
	init_db.py : 
		Permet d'intialiser la base de données
	start1.py :
	   	Permet de démarrer le site:
	start2.py : 
	      	Permet de démarrer la station



