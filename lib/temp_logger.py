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

    def __init__(self, location="Default"):
        """Initialize the logger."""
        self.__wifi = WifiManager(secrets.ssid, secrets.password)
        self.__dht = DHTManager(gpio_pin=15)
        self.__sd_card = SDManager(baudrate=1_000_000)
        self.__location = location
        self.__wifi.connect()
        self.__sd_card.mount()

    def __str__(self):
        """String output."""
        (year, month, day, hour, minute, second) = time.localtime()[:6]
        return (f"{self.__location}\n"
                f"{str(self.__dht.get_temp_c())}*C,\n"
                f"{str(self.to_fahrenheit(self.__dht.get_temp_c()))}*F,\n"
                f"{str(self.__dht.get_humidity())}%\n"
                f"{month:02}/{day:02}/{year}, {hour:02}:{minute:02}:{second:02}"
                )

    def to_fahrenheit(self, celsius):
        """Calculte fahrenheit based on celsius."""
        return celsius * 9.0 / 5.0 + 32.0

    def to_json(self):
        """Output JSON."""
        return json.dumps({
            'celsius': self.__dht.get_temp_c(),
            'fahrenheit': self.to_fahrenheit(self.__dht.get_temp_c()),
            'humidity': self.__dht.get_humidity(),
            'date': time.localtime()
        })

    def to_csv(self):
        """Writes to a CSV file."""
        try:
            with open('/sd/logger.csv', 'a') as outfile:
                temp_c = self.__dht.get_temp_c()
                temp_f = self.to_fahrenheit(temp_c)
                humidity = self.__dht.get_humidity()
                timex = time.localtime()
                outfile.write(f"{self.__location},{temp_c},{temp_f},{humidity},{timex}\n")
        except OSError as e:
            print(f"Exception: {e}")

    def get_location(self):
        """Getter for location."""
        return self.__location

    def get_ip(self):
        """Getter for IP."""
        return self.__wifi.ip_addr_show()
