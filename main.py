from temp_logger import TempLogger
from microdot import Microdot, Response, send_file
import uasyncio
import time
import os

logger = TempLogger("Office", 1)

app = Microdot()

@app.route("/")
async def index(request):
    return str(logger)

@app.route("/api/v2/json")
async def json(request):
    return Response(body=logger.to_json(),
                    headers={'Content-Type': 'application/json'})

@app.route("/api/v2/csv")
async def csv(request):
    data = logger.sd_card.read_sd("logger.csv")
    return Response(body=data,
                    headers={'Content-Type': 'text/csv',
                             "Content-Disposition": 'attachment; filename="logger.csv"'})

@app.route("/api/v2/min")
async def min(request):
    return str(logger.dht.get_min())

@app.route("/api/v2/max")
async def max(request):
    return str(logger.dht.get_max())

async def background_loop():
    while True:
        try:
            logger.dht._measure()
            if logger.wifi.get_actual_time()[4] % 5 == 0:
                logger.sd_card.write_sd("logger.csv", logger.to_csv())
            #if logger.dht.get_min() != None and logger.dht.get_min() < logger.dht.get_temp_c():
            #    logger.sd_card.write_sd("min.txt", logger.dht.get_min())
            #if logger.dht.get_max() != None and logger.dht.get_max() > logger.dht.get_temp_c():
            #    logger.sd_card.write_sd("max.txt", logger.dht.get_max())
        except OSError as e:
            print(f"Background error: {e}")
            break
        await uasyncio.sleep(logger.sleep_min)
        
async def main():
    print("main()")
    uasyncio.create_task(background_loop())
    print("Started background_loop CSV logging...")
    await app.start_server(port=5000)
    
try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
