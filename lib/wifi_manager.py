import network
import time

class WifiManager:
    def __init__(self, ssid, password, retries=10, delay=2):
        self.__ssid = ssid
        self.__password = password
        self.__retries = retries
        self.__delay = delay

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self):
        while not self.wlan.isconnected():
            print(f"Connecting to {self.__ssid}...")
            self.wlan.connect(self.__ssid, self.__password)
            time.sleep(1)
        else:
            print(f"Connected to {self.__ssid}.")

        return self.wlan.isconnected()

    def disconnect(self):
        while self.wlan.isconnected():
            self.wlan.disconnect()
        else:
            print(f"Disconnected from {self.__ssid}")

    def ip_addr_show(self):
        if self.wlan.isconnected():
            # 0 - IP Addr
            # 1 - Netmask
            # 2 - Gateway
            # 3 - DNS
            return self.wlan.ifconfig()
        return None
