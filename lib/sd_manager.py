"""
Handles creating an SDManager instance, mounting, unmounting, and
a write function, to write data to specified file.
"""
import machine
import sdcard
import uos


class SDManager:
    """Handle the SD Card module."""

    def __init__(self, spi_id=1, sck=10,
                 mosi=11, miso=12, cs=13, baudrate=1_000_000):
        """Handle all SDCard module configuration."""
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
        self.sd = None
        self.vfs = None
        self.mount_point = "/sd"

    def mount(self, mount_point="/sd"):
        """Create mount point."""
        try:
            self.sd = sdcard.SDCard(self.spi, self.cs)
            self.vfs = uos.VfsFat(self.sd)
            uos.mount(self.vfs, mount_point)
        except OSError as e:
            print(f"Failed to mount SD Card: {e}")
        else:
            print(f"SD Card mounted at {mount_point}")

    def umount(self, mount_point="/sd"):
        """Unmount."""
        try:
            uos.umount(mount_point)
        except OSError as e:
            print(f"Failed to unmount: {e}")
        else:
            print(f"Unmounted: {mount_point}")

    def write(self, text, mount_point="/sd"):
        """Writes to specified file at mount point."""
        try:
            with open(f"{mount_point}/logger.txt", "a") as file:
                file.write(text + "\n")
                file.flush()
        except Exception as e:
            print(f"Error writing file: {e}")
        else:
            print("Wrote data.")
