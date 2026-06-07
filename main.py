"""
Using a Raspberry Pi Pico W, SD Card module, and a DHT11
temperature sensor, we have a working temperature logger.
It logs to a CSV file, web interface, and a json end-point.
"""
from temp_logger import TempLogger
from microdot import Microdot, Response, send_file
import uasyncio
import os

logger = TempLogger("Garage")

if logger.get_ip():
    print(logger.get_ip()[0])

app = Microdot()


@app.route('/')
async def index(request):
    """Index function."""
    return str(logger)


@app.route('/api/v1/json')
async def json(request):
    """Return JSON formatted temperature data."""
    return Response(body=logger.to_json(),
                    headers={'Content-Type': 'application/json'})

@app.route('/api/v1/csv')
async def csv(request):
    """Send a .csv formatted file to browser."""
    print(os.listdir())
    return send_file("sd/logger.csv")


async def background_loop():
    """Background loop to continually log to CSV file."""
    while True:
        try:
            logger.to_csv()
        except OSError as e:
            print(f"Background error: {e}")
            break
        await uasyncio.sleep(60)


async def main():
    """Runs automatically when the Pico initializes after boot."""
    print("Starting server...")
    uasyncio.create_task(background_loop())
    print("Started background_loop CSV logging...")
    await app.start_server(port=5000)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
