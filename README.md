# Raspberry Pi Pico W - Temperature Monitor
This package runs on a Raspberry Pi Pico W and provides a web interface to view temperature information collected by the DHT11 module.  Along with an SD Card adapter, this package logs the data to a CSV file on the SD card.  There are a few API endpoints:
```
- Web Interface:		
	- http://ip-address:5000/
- JSON Output:
	- http://ip-address:5000/api/v2/json 
- Download a CSV file:	
	- http://ip-address:5000/api/v2/csv 
```
```
I created:
- lib/dht_manager.py
- lib/sd_manager.py
- lib/temp_logger.py
- lib/wifi_manager.py
- main.py
```
```
microdot.py and sdcard.py are not written by me.
```