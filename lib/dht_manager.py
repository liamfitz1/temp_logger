import time
import machine
import dht
from machine import Pin

led = Pin("LED", Pin.OUT)
def blink_led(led):
    for _ in range(3):
        led.on()
        time.sleep(1)
        led.off()

class DHTManager:
    
    def __init__(self, gpio_pin):
        self.sensor = dht.DHT11(machine.Pin(gpio_pin))
        self.temperature = None
        self.humidity = None
        self.min_temp = None
        self.max_temp = None
        self.__last_measure = 0
        self._measure()
        
    def _measure(self, retries=5):
#         blink_led(led)
        for _ in range(retries):
            if time.ticks_diff(time.ticks_ms(), self.__last_measure) >= 2000:
                try:
                    self.sensor.measure()
                    self.temperature = self.sensor.temperature()
                    self.humidity = self.sensor.humidity()
                    if self.min_temp == None or self.temperature < self.min_temp:
                        self.min_temp = self.temperature
                    if self.max_temp == None or self.temperature > self.max_temp:
                        self.max_temp = self.temperature
                    self.__last_measure = time.ticks_ms()
                except OSError as e:
                    print(f"DHT read failed: {e}")
                else:
                    print(f"Measurement OK: {self.temperature} {self.humidity}")
                    print(f"Min/Max OK: {self.min_temp} {self.max_temp}")
                    print(f"Last Measure: {self.__last_measure}")
                    break
            else:
                time.sleep(2)
                
    def get_temp_c(self):
        if self.temperature != None:
            return self.temperature
        return False
    
    def get_temp_f(self):
        if self.temperature != None:
            return float(self.temperature) * 9.0 / 5.0 + 32.0
        return False
    
    def get_humidity(self):
        if self.humidity != None:
            return self.humidity
        return False
    
    def get_min(self):
        if self.min_temp:
            return self.min_temp
        return None
    
    def get_max(self):
        if self.max_temp:
            return self.max_temp
        return None
    
    def to_f(self, celcius):
        return float(celcius) * 9.0 / 5.0 + 32.0

if __name__ == "__main__":
    dht_manager = DHTManager(gpio_pin=15)
    dht_manager._measure()
    print(f"Temp C: {dht_manager.get_temp_c()}")
    print(f"Temp F: {dht_manager.get_temp_f()}")
    print(f"Humidity: {dht_manager.get_humidity()}")
    print(f"Min Temp C: {dht_manager.get_min()}")
    print(f"Max Temp C: {dht_manager.get_max()}")
    print(f"Min Temp F: {dht_manager.to_f(dht_manager.get_min())}")
    print(f"Max Temp F: {dht_manager.to_f(dht_manager.get_max())}")
