import asyncio
import SiteStation.siteStation as siteStation
asyncio.create_task(siteStation.run())

import Raspberry.init as capteurs
asyncio.create_task(capteurs.run())