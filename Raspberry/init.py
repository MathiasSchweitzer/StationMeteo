import os
import station
import sqlite3


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), 'data.db')
    sql_path = os.path.join(os.path.dirname(__file__), 'tables.sql')
    if not os.path.isfile(path): #Pas de fichier data.db

        #On crée aussi le fichier log.txt
        if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'log.txt')):
            f = open(os.path.join(os.path.dirname(__file__), 'log.txt'),'w')
            f.close()
        station.log("Création de la base de données...")
        conn = sqlite3.connect(path)
        with open('tables.sql','r') as query:
            conn.execute(query.read())
        conn.commit()
        conn.close()
        station.log("Fichier data.db créé")
        #On démarre le programe en tant que premier démarrage, le programme ne démarrera pas avant 00h00
        station.start(firstboot=True)
    else:
        station.start()
        

