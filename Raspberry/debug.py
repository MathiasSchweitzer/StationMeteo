
from datetime import datetime, timedelta
import time
import threading
import sqlite3
import capteurs
import os
import station
 




def __debug(txt):
    print(station.format(),txt)


def info():

    humidite = temp_dps = temp_dht22 = pression = lumiere = 'ERREUR'
    hascrashed = False

    RED = '\033[91m'
    RESET = '\033[0m'

    #RECUPERATION HUMIDITE
    try:
        humidite = capteurs.humidite()
    except Exception as e:
        __debug(RED + "Erreur lors de la récupération de l'humidité avec le capteur DHT22" + RESET)
        __debug(e)
        hascrashed = True
    

    #RECUPERATION TEMPERATURE DPS310
    try:
        temp_dps = capteurs.temperature_DPS310()
    except Exception as e:
        __debug(RED + "Erreur lors de la récupération de la température avec le capteur DPS310" + RESET)
        __debug(e)
        hascrashed = True
    

    #RECUPERATION TEMPERATURE DHT22
    try:
        temp_dht22 = capteurs.temperature_DHT22()
    except Exception as e:
        __debug(RED + "Erreur lors de la récupération de la température avec le capteur DHT22" + RESET)
        __debug(e)
        hascrashed = True


    #RECUPERATION LUMIERE
    try:
        lumiere = capteurs.lumiere()
    except Exception as e:
        __debug(RED + "Erreur lors de la récupération de la lumière avec le capteur Grove - Light Sensor" + RESET)
        __debug(e)
        hascrashed = True
    
    #RECUPERATION PRESSION
    try:
        pression = capteurs.pression()
    except Exception as e:
        __debug(RED + "Erreur lors de la récupération de la pression atmosphérique avec le capteur DPS310" + RESET)
        __debug(e)
        hascrashed = True

    __debug(f"Température : DPS310 : {temp_dps} / DHT22 : {temp_dht22} | Humidité : {humidite} | Pression : {pression} | Lumière : {lumiere}")
    if(hascrashed):
        print("")


    




    

if __name__ == '__main__':
    while True:

        intervalle = 5 #On veut récuperer les informations toutes les X secondes
        start_time = time.time()

        thread = threading.Thread(target=info)
        thread.start()
        thread.join()

        end_time = time.time()
        execution_time = end_time-start_time
        time_to_sleep = max(intervalle-execution_time,0)
        time.sleep(time_to_sleep)