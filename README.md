Contenu des fichiers de code :

Site :

	graphique.js :
    	Contient le code nécessaire à la création des graphiques ainsi que le changement du graphique sélectionné en appuyant sur les boutons.

	global.js :
    	Contient le code utile à plusieurs pages : flèches pour naviguer à l'élément précédent / suivant, la fonction de recherche, le bouton "Aujourd'hui" et les mois et jours des calendriers qui ouvrent l'élément correspondant.

	index.py :
		Contient le code pour héberger le site et l'adaptabilité des pages en fonction des données.


Raspberry : 

 	debug.py : 

 		Permet de visualiser les données en temps réel, permet aussi de déboguer en affichant les potentiels erreurs des capteurs.

   	capteurs.py :

     		Fichier indispensable qui permet de récupérer les données des capteurs.

	init.py : 

 		Fichier qui doit être lancé lorsque l'on veut démarrer la station.

   	station.py : 

    		Permet de lancer la station, ne pas utiliser ce fichier lors de la première initialisation
