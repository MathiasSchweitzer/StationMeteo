import os
import Raspberry.station as station
import sqlite3

def run():
    if not os.path.isfile(station.path_log):
        f = open(station.path_log,'w')
        f.close()
    station.start()

if __name__ == '__main__':
    run()

