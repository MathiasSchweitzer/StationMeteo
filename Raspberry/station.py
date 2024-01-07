from datetime import datetime, timedelta
import time
import threading
import sqlite3
import Raspberry.capteurs as capteurs
import os

path_db = 'data.db'
path_log = 'log.txt'
path_sql = 'tables.sql'

async def log(txt):
    with open(path_log, 'a',encoding='utf-8') as file:
        file.write(format()+f" {txt}\n")
    print(format(),txt)
async def format():
    c = datetime.now()
    yyyy = c.year
    mm = c.month
    dd = c.day
    hrs = c.hour
    minute = c.minute
    s = c.second
    return f"[{dd:02d}/{mm:02d}/{yyyy} à {hrs:02d}:{minute:02d}:{s:02d}]"

def __mainf():
    path = os.path.join(path_db)
    conn = sqlite3.connect(path)
    query = 'INSERT OR REPLACE INTO data (dateDonnee, heure, typeDonnee, donnee) VALUES (?, ?, ?, ?)'
    current_date = datetime.now()
    date = str(current_date.year)+str(current_date.month).zfill(2)+str(current_date.day).zfill(2)
    heure = str(current_date.hour).zfill(2)+str(current_date.minute).zfill(2)
    conn.execute(query, (date, heure, 'lumiere', capteurs.lumiere()))
    conn.execute(query, (date, heure, 'pression', capteurs.pression()))
    conn.execute(query, (date, heure, 'temp1', capteurs.temperature_DHT22()))
    conn.execute(query, (date, heure, 'temp2', capteurs.temperature_DPS310()))
    conn.execute(query, (date, heure, 'humidite', capteurs.humidite()))
    conn.commit()
    conn.close()

async def start(firstboot=False):
    if firstboot:
        #On veut démarrer le programme la prochaine journée à 00h00 pour avoir des données complètes
        await log('En attente de 00h00...')
        now = datetime.now()
        next_day = datetime(now.year, now.month, now.day) + timedelta(days=1)
        waitt = (next_day - now).total_seconds()
        threading.Timer(waitt, lambda: start()).start()

    else:
        await log("Démarrage du programme")
        while True:
            start_time = time.time()

            #On utilise le multithreading pour empêcher le programme de se stopper en cas d'erreur
            thread = threading.Thread(target=__mainf)
            thread.start()
            thread.join()
            await log('Données enregistrées')
            end_time = time.time()
            execution_time = end_time - start_time
            #Pour que le programme s'effectue toutes les minutes, on a besoin de soustraire
            #60 moins le temps d'exécution, sans cela, 
            #le programme finira par sauter une minute plusieurs fois par jour
            time_to_sleep = max(60 - execution_time, 0)
            time.sleep(time_to_sleep)
        

if __name__ == '__main__':
    start()