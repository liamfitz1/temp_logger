import time
import ntptime
import network


class WifiManager:
    def __init__(self, ssid, password, delay=2):
        self.ssid = ssid
        self.password = password
        self.delay = delay
        self.ip = None
        self.utc_time = None
        self.actual_time = None
        self.UTC_OFFSET = -7 * 60 * 60
    
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected():
            print("Waiting for connection...")
            time.sleep(self.delay)
            
        self.ip = self.wlan.ifconfig()[0]
        print(f"Connected on: {self.ip}")
        
        while True:
            try:
                ntptime.settime()
                print(f"NTP (UTC) Time: {time.localtime()}")
                self.utc_time = time.localtime()
            except Exception as e:
                print(f"NTP Failed: {e}")
                time.sleep(5)
            else:
                self.actual_time = time.localtime(time.time() + self.UTC_OFFSET)
                print(f"LOCAL TIME: {self.actual_time}")
                break
        
        return self.ip
    
    def ip_addr(self):
        if self.wlan.isconnected() and self.ip != None:
            return self.ip
        return None
    
    def get_actual_time(self):
        self.actual_time = time.localtime(time.time() + self.UTC_OFFSET)
        return self.actual_time
    
if __name__ == "__main__":
    wifi_man = WifiManager("change_me","change_me")
    wifi_man.connect()
    print(f"IP: {wifi_man.ip_addr()}")