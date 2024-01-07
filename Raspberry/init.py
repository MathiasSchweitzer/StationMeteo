import os
import Raspberry.station as station
import asyncio

async def run():
    if not os.path.isfile(station.path_log):
        f = open(station.path_log,'w')
        f.close()
    asyncio.create_task(station.start())

if __name__ == '__main__':
    run()

