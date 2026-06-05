"""
Connect the Pico to a network.
"""
import time
import network


class WifiManager:
    """Wifi manager handles init, connect, disconnect, and ip info."""

    def __init__(self, ssid, password, retries=10, delay=2):
        """Initializer, uses the lib/secrets.py file with wifi info."""
        self.__ssid = ssid
        self.__password = password
        self.__retries = retries
        self.__delay = delay
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self):
        """Connects to the network."""
        while not self.wlan.isconnected():
            print(f"Connecting to {self.__ssid}...")
            self.wlan.connect(self.__ssid, self.__password)
            time.sleep(1)
        print(f"Connected to {self.__ssid}.")
        return self.wlan.isconnected()

    def disconnect(self):
        """Disconnects from the network."""
        while self.wlan.isconnected():
            self.wlan.disconnect()
            time.sleep(1)
        print(f"Disconnected from {self.__ssid}")

    def ip_addr_show(self):
        """Provides ip address information."""
        if self.wlan.isconnected():
            # 0 - IP Addr
            # 1 - Netmask
            # 2 - Gateway
            # 3 - DNS
            return self.wlan.ifconfig()
        return None
