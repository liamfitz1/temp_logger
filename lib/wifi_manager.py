import time
import ntptime
import network


class WifiManager:
    def __init__(self, ssid, password, retries=10, delay=2):
        self.ssid = ssid
        self.password = password
        self.retries = retries
        self.delay = delay
        self.wlan = network.WLAN(network.STA_IF)

        # activates wlan 'up'
        self.wlan.active(True)

    def connect(self):
        while not self.wlan.isconnected():
            print(f"Connecting to {self.ssid}...")
            self.wlan.connect(self.ssid, self.password)
            time.sleep(self.delay)
        print(f"Connected to {self.ssid}!")
        return self.wlan.isconnected()

    def disconnect(self):
        while self.wlan.isconnected():
            print(f"Disconnecting from {self.ssid}...")
            self.wlan.disconnect()
            time.sleep(self.delay)
        print(f"Disconnected from {self.ssid}!")
        self.wlan.active(False)
        return self.wlan.isconnected()

    def ip_addr(self):
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return None
