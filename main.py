from temp_logger import TempLogger
from microdot import Microdot, Response
import uasyncio

logger = TempLogger("Garage")

if logger.get_ip():
    print(logger.get_ip()[0])

app = Microdot()

@app.route('/')
async def index(request):
    return str(logger)

@app.route('/api/v1/json')
async def json(request):
    return Response(body=logger.to_json(),
                    headers={'Content-Type': 'application/json'})

async def background_loop():
    while True:
        try:
            logger.to_csv()
        except Exception as e:
            print(f"Background error: {e}")
        await uasyncio.sleep(10)

async def main():
    print("Starting server...")
    uasyncio.create_task(background_loop())
    print("Started background_loop CSV logging...")
    await app.start_server(port=5000)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()