"""
Using a Raspberry Pi Pico W, SD Card module, and a DHT11
temperature sensor, we have a working temperature logger.
It logs to a CSV file, web interface, and a json end-point.
"""
from temp_logger import TempLogger
from microdot import Microdot, Response, send_file
#from microdot.utemplate import Template
import uasyncio
import time
import os
from machine import Pin

led = Pin("LED", Pin.OUT)
def debug_led(led):
	led.on()
	time.sleep(1)
	led.off()


# TempLogger( Location, Minutes )
logger = TempLogger("Garage", 5)


if logger.get_ip():
    print(logger.get_ip())
    debug_led(led)

	
app = Microdot()


@app.route('/')
async def index(request):
    """Index function."""
    debug_led(led)
    return str(logger)
    #return Template('index.html').render(logger=str(logger))


@app.route('/api/v1/json')
async def json(request):
    """Return JSON formatted temperature data."""
    return Response(body=logger.to_json(),
                    headers={'Content-Type': 'application/json'})

@app.route('/api/v1/csv')
async def csv(request):
    with open(logger.__sd_card.filename, 'r') as f:
        data = f.read()

    return Response(
        data,
        headers={
            'Content-Type': 'text/csv'
        }
    )

async def background_loop():
    """Background loop to continually log to CSV file."""
    if logger.is_mounted():
        while True:
            try:
                logger.to_csv()
                print("logged to CSV file.")
                debug_led(led)
            except OSError as e:
                print(f"Background error: {e}")
                break
            await uasyncio.sleep(logger.get_sleep())
    else:
        print("Not mounted. background_loop()")

async def main():
    """Runs automatically when the Pico initializes after boot."""
    print(f"Localtime sync: {time.localtime()}")
    print("Starting server...")
    uasyncio.create_task(background_loop())
    print("Started background_loop CSV logging...")
    await app.start_server(port=5000)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
