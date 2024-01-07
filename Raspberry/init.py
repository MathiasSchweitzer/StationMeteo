import os
import Raspberry.station as station
import sqlite3

def run():
    if not os.path.isfile(station.path_db): #Pas de fichier data.db

        #On crée aussi le fichier log.txt
        if not os.path.isfile(station.path_log):
            f = open(station.path_log,'w')
            f.close()
        station.log("Création de la base de données...")
        conn = sqlite3.connect(station.path_db)
        with open('tables.sql','r') as query:
            conn.execute(query.read())
        conn.commit()
        conn.close()
        station.log("Fichier data.db créé")
        #On démarre le programe en tant que premier démarrage, le programme ne démarrera pas avant 00h00
        station.start(firstboot=True)
    else:
        station.start()

if __name__ == '__main__':
    run()

