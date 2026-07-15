import secrets
import json
import time

from wifi_manager import WifiManager
from dht_manager import DHTManager
from sd_manager import SDManager
from machine import Pin

led = Pin("LED", Pin.OUT)
def blink_led(led, count=1):
    for _ in range(count):
        led.on()
        time.sleep(1)
        led.off()
    
class TempLogger:

    def __init__(self, location="Default", sleep_min=1):
        self.wifi = WifiManager(secrets.ssid, secrets.password, delay=2)
#         blink_led(led, 2)
        self.dht = DHTManager(gpio_pin=15)
#         blink_led(led, 3)
        self.sd_card = SDManager(baudrate=1_000_000)
#         blink_led(led, 4)
        self.location = location
        self.sleep_min = sleep_min * 60
        
#         blink_led(led, 5)
        self.wifi.connect()
#         blink_led(led, 6)
        self.sd_card.mount_sd()
        
        with open(f"{self.sd_card.mount_point}/logger.csv", "a") as f:
            pass
        
    def __str__(self):
        return (
            f"Temp C: {self.dht.get_temp_c()}\n"
            f"Temp F: {self.dht.get_temp_f()}\n"
            f"Humidity: {self.dht.get_humidity()}\n"
            f"Min C: {self.dht.get_min()}\n"
            f"Min F: {self.dht.to_f(self.dht.get_min())}\n"
            f"Max C: {self.dht.get_max()}\n"
            f"Max F: {self.dht.to_f(self.dht.get_max())}\n"
            f"Time: {self.wifi.get_actual_time()}\n"
        )
    
    def to_json(self):
        return json.dumps({
            'celsius': self.dht.get_temp_c(),
            'fahrenheit': self.dht.to_f(self.dht.get_temp_c()),
            'humidity': self.dht.get_humidity(),
            'time': self.wifi.get_actual_time(),
            'max_f': self.dht.to_f(self.dht.get_max()),
            'min_f': self.dht.to_f(self.dht.get_min()),
            'max_c': self.dht.get_max(),
            'min_c': self.dht.get_min()
        })
    
    def to_csv(self):
#         blink_led(led)
        return (
            f"{self.location},"
            f"{self.dht.get_temp_c()},"
            f"{self.dht.to_f(self.dht.get_temp_c())},"
            f"{self.dht.get_humidity()},"
            f"{self.dht.get_min()},"
            f"{self.dht.get_max()},"
            f"{self.wifi.get_actual_time()}"
        )
    
if __name__ == "__main__":
    temp_logger = TempLogger("Office",1)
    print(f"{temp_logger.to_json()}")
    print(f"{temp_logger.to_csv()}")
