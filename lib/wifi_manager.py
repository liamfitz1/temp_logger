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

    def connect(self, timeout_s=20):
        self.wlan.active(True)

        if not self.wlan.isconnected():
            print(f"Connecting to {self.ssid}...")
            self.wlan.connect(self.ssid, self.password)

        start = time.ticks_ms()
        while not self.wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), start) > timeout_s * 1000:
                print("WiFi connect timed out")
                return False
            time.sleep(0.5)

        print(f"Connected to {self.ssid}!")
        # Sets RTC to UTC
        try:
            ntptime.settime()
            print("NTP (UTC) time:", time.localtime())
        except Exception as e:
            print("NTP failed:", e)

        return True

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
