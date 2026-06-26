"""
Main object of the program.  Handles temperature sensor data and output.
"""
import secrets
import json
import time

from wifi_manager import WifiManager
from dht_manager import DHTManager
from sd_manager import SDManager


class TempLogger:
    """Main object for the program."""

    def __init__(self, location="Default", sleep_min=1):
        """Initialize the logger."""
        self.__wifi = WifiManager(secrets.ssid, secrets.password)
        self.__dht = DHTManager(gpio_pin=15)
        self.__sd_card = SDManager(baudrate=1_000_000)
        self.__location = location
        self.__sleep_min = sleep_min
        self.__wifi.connect()
        print(f"LOCAL TIME: {self.get_date()}")
        self.__sd_card.mount_sd()


    def __str__(self):
        """String output."""
        return (f"{self.__location}\n"
                f"{str(self.__dht.get_temp_c())}*C,\n"
                f"{str(self.to_fahrenheit(self.__dht.get_temp_c()))}*F,\n"
                f"{str(self.__dht.get_humidity())}%\n"
                f"{self.get_date()}\n"
                f"Min: {self.__dht.get_min()}*C\n"
                f"Max: {self.__dht.get_max()}*C\n"
                f"Min *F: {self.to_fahrenheit(self.__dht.get_min())}*F\n"
                f"Max *F: {self.to_fahrenheit(self.__dht.get_max())}*F\n"
        )

    def to_fahrenheit(self, celsius):
        """Calculte fahrenheit based on celsius."""
        return celsius * 9.0 / 5.0 + 32.0

    def to_json(self):
        """Output JSON."""
        return json.dumps({
            'celsius': self.__dht.get_temp_c(),
            'min_celsius': self.__dht.get_min(),
            'max_celsius': self.__dht.get_max(),
            'fahrenheit': self.to_fahrenheit(self.__dht.get_temp_c()),
            'min_fahrenheit': self.to_fahrenheit(self.__dht.get_min()),
            'max_fahrenheit': self.to_fahrenheit(self.__dht.get_max()),
            'humidity': self.__dht.get_humidity(),
            'date': self.get_date()
        })

    def to_csv(self):
        """Writes to a CSV file."""
        if self.__sd_card.is_mounted:
            try:
                with open(self.__sd_card.filename, 'a') as outfile:
                    temp_c = self.__dht.get_temp_c()
                    temp_f = self.to_fahrenheit(temp_c)
                    humidity = self.__dht.get_humidity()
                    current_time = self.get_date()
                    outfile.write(
                        f"{self.__location},"
                        f"{temp_c},{temp_f},"
                        f"{humidity},{current_time},"
                        f"{self.__dht.get_min()},"
                        f"{self.to_fahrenheit(self.__dht.get_min())},"
                        f"{self.__dht.get_max()},"
                        f"{self.to_fahrenheit(self.__dht.get_max())}\n"
                    )
            except OSError as e:
                print(f"Exception: {e}")
        else:
            print("Not mounted. write()")

    def get_location(self):
        """Getter for location."""
        return self.__location

    def get_ip(self):
        """Getter for IP."""
        return self.__wifi.ip_addr()

    def get_date(self):
        """Getter for date."""
        (year, month, day, hour, minute, second) = time.localtime()[:6]
        return f"{month:02}/{day:02}/{year},{hour:02}:{minute:02}:{second:02}"

    def get_sleep(self):
        return 60 * self.__sleep_min
    
    def is_mounted(self):
        return self.__sd_card.is_mounted
    
    def write_min_max(self):
        if self.__sd_card.is_mounted:
            try:
                with open(self.__sd_card.min_max, 'w+') as outfile:
                    (min, max) = (self.__dht.get_min(), self.__dht.get_max())
                    outfile.write(f"{min},{max}")
            except OSError as e:
                print(f"Exception: {e}")
                
    def read_min_max(self):
        if self.__sd_card.is_mounted:
            try:
                with open(self.__sd_card.min_max, 'r+') as infile:
                    (min, max) = infile.read().split(',')
                    print(f"min: {min}, max: {max}")
            except OSError as e:
                print(f"Exception in READ: {e} {self.__sd_card.min_max}")