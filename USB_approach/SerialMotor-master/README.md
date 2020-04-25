# SerialMotor
Uses pyserial to control motors on a connected Arduino with an attached Adafruit Motor Shield v1.

Requires `pyserial`. Installation instructions [here](https://pyserial.readthedocs.io/en/latest/pyserial.html).

I recommend running `pip install pyserial` from the command line.

Arduino may show up as a different address, such as /dev/ttyCM0

use lshw library or dmesg to confirm

command line example: dmesg | grep -i usb

must have strong battery power for arudino and pi to run


