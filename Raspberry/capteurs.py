import GroveLightSensor as Grove
import seeed_dht
import DPS

sensor_dht = seeed_dht.DHT("22", 22)
sensor_light = Grove.GroveLightSensor(0)
dps310 = DPS.DPS()

def humidite():
    '''
    Capteur utilisé : Grove - Temperature & Humidity Sensor Pro (DHT22)
    '''
    return round(sensor_dht.read()[0],1)

def lumiere():
    '''
    Capteur utilisé : Grove - Light Sensor
    '''
    return sensor_light.light
def pression():
    '''
    Capteur utilisé : Grove - High Precision Barometric Pressure Sensor (DPS310)
    '''
    scaled_p = dps310.calcScaledPressure()
    scaled_t = dps310.calcScaledTemperature()
    return round(dps310.calcCompPressure(scaled_p,scaled_t)/100,1)
def temperature_DHT22():
    '''
    Capteur utilisé : Grove - Temperature & Humidity Sensor Pro (DHT22)
    '''
    return round(sensor_dht.read()[1],1)
def temperature_DPS310():
    '''
    Capteur utilisé : Grove - High Precision Barometric Pressure Sensor (DPS310)
    '''
    return round(dps310.calcCompTemperature(dps310.calcScaledTemperature()),1) 