import secrets
import json
import ntptime
import time

from wifi_manager import WifiManager
from dht_manager import DHTManager
from sd_manager import SDManager
from microdot import Microdot

class TempLogger:
    def __init__(self, location="Default"):
        self.__wifi = WifiManager(secrets.ssid, secrets.password)
        self.__dht = DHTManager(gpio_pin=15)
        self.__sd_card = SDManager(baudrate=1_000_000)
        self.__location = location

        self.__wifi.connect()

        self.__sd_card.mount()
        
    def __str__(self):
        return (f"{self.__location}\n"
            f"{str(self.__dht.get_temp_c())}*C,\n"
            f"{str(self.to_fahrenheit(self.__dht.get_temp_c()))}*F,\n"
            f"{str(self.__dht.get_humidity())}%\n"
            f"{time.localtime()}"
        )
    
    def to_fahrenheit(self, celcius):
        return celcius * 9.0 / 5.0 + 32.0
    
    def to_json(self):
        return json.dumps({
            'celcius': self.__dht.get_temp_c(),
            'fahrenheit': self.to_fahrenheit(self.__dht.get_temp_c()),
            'humidity': self.__dht.get_humidity(),
            'date': time.localtime()
        })
    
    def to_csv(self):
        try:
            with open('/sd/logger.csv', 'a') as outfile:
                temp_c = self.__dht.get_temp_c()
                temp_f = self.to_fahrenheit(temp_c)
                humidity = self.__dht.get_humidity()
                timex = time.localtime()
                outfile.write(f"{self.__location},{temp_c},{temp_f},{humidity},{timex}\n")
        except Exception as e:
            print(f"Exception: {e}")
    
    def get_location(self):
        return self.__location
    
    def get_ip(self):
        return self.__wifi.ip_addr_show()