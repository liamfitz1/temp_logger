import machine
import vfs
import sdcard
from machine import Pin

led = Pin("LED", Pin.OUT)
def blink_led(led, count):
    for _ in range(count):
        led.on()
        time.sleep(0.5)
        led.off()

class SDManager:
    def __init__(
        self,
        spi_id=1,
        sck=10,
        mosi=11,
        miso=12,
        cs=13,
        baudrate=1_000_000,
        mnt="/mnt",
        log_file="log_file.txt",
        csv_file="csv_file.csv",
        min_max_file="min_max.txt"
        ):
        self.spi = machine.SPI(
            spi_id,
            baudrate,
            polarity=0,
            phase=0,
            sck=machine.Pin(sck),
            mosi=machine.Pin(mosi),
            miso=machine.Pin(miso)
        )
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.sd_card = None
        self.vfs = None
        self.mount_point = mnt
        self.is_mounted = False
        # os.path.join not available in micropython
        self.log_file = f"{self.mount_point}/{log_file}"
        self.csv_file = f"{self.mount_point}/{csv_file}"
        self.min_max = f"{self.mount_point}/{min_max_file}"

    def mount_sd(self):
        if not self.is_mounted:
            try:
                self.sd_card = sdcard.SDCard(self.spi, self.cs)
                self.vfs = vfs.VfsFat(self.sd_card)
                vfs.mount(self.vfs, self.mount_point)
                self.is_mounted = True
            except OSError as e:
                print(f"Unable to mount {self.mount_point}: {e}")
                blink_led(led, 4)        
            print(f"Mounted: {self.mount_point}")
        else:
            print("Already mounted.")

    def unmount_sd(self):
        if self.is_mounted:
            try:
                vfs.umount(self.mount_point)
                self.sd_card = None
                self.vfs = None
                self.is_mounted = False
            except OSError as e:
                print(f"Unable to unmount {self.mount_point}: {e}")
            print(f"Unmounted: {self.mount_point}")
        else:
            print("Already unmounted.")

    def write_sd(self, filename, data):
        if not self.is_mounted:
            self.mount_sd()

        try:
            with open(f"{self.mount_point}/{filename}", "a") as f:
                f.write(data + "\n")
        except Exception as e:
            print(f"Error writing file: {e}")
            blink_led(led, 6)   
        else:
            print("Wrote data.")

    def read_sd(self, filename):
        if not self.is_mounted:
            self.mount_sd()

        try:
            with open(f"{self.mount_point}/{filename}", "r") as f:
                while True:
                    chunk = f.read(512)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            print(f"Error reading file: {e}")
        else:
            print("Read data.")


if __name__ == "__main__":
    sd_man = SDManager()
    sd_man.mount_sd()
    sd_man.write_sd("log_file.txt", "TEST DATA")
    sd_man.read_sd("log_file.txt")
    sd_man.read_sd("min_max.txt")
    sd_man.unmount_sd()
    