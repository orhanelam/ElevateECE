TO GET ROBOT MOVING:


HARDWARE:

Connect pin 6 of your rasberry pi to the ground of the Arduino. Connect pins 12 and 18 (NOT the GPIO pins, the actual pins per pi_pin_insertion_guide.png attached above) of the the pi to A0 and A1 of the arduino, respectively.
Power the Pi by connecting the outputs of the voltage regulator to power and ground pins on the Pi.
Please see the 3 images in root directory for further explanations on wiring


SOFTWARE:

Upload the .ino file into your arduino. There are a couple changes from the old motor-controller code, so please re-upload this one to make sure everything works. Make sure to download the Adafruit Motor library.
Load the python script "MotorController.py" into your rasberry pi, into the same directory as your python code that will give out movement commands. I've included an example file uses the commands properly.


CALIBRATION:

You shouldn't ever need to to change the .ino file, but the python file uses experimentally-derived constants for the movement, which may be different for your bot. The test code is designed to have the bot turn 90 degrees right twice, then back 90 degrees left twice, and then go forward two meters, each action with a one second delay. But if the bot doesn't do the above, i.e. it turns too little or too much or moves too far, you'll need to change the constants. If so change the 'turnConstant' and 'moveConstant' parameters until the bot does the above. Roughly you should be able to adjust each with the following process:

moveConstant:

1. Measure actual distance covered in meters.
2. Divide 2 meters by the actual distance.
3. Multiply previous moveConstant by this to get the new moveConstant.

turnConstant: 

1. Measure actual right angle turned in degrees.
2. Divde 180 degrees by actual angle.
3. Multiply previous turnConstant by this to get the new turnConstant. 

runOnStartup:

1. On command line execute 'sudo nano /etc/rc.local'
2. Erase IP address logging code (default) and replace with 'python /home/pi/re$
3. Make sure the ampersand is there (it tells the Pi to continue loading progra$
4. Ctrl+X will save, Y, and enter will get you back to command line

IMU Setup:

1. https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/pinouts
2. Connect the SCL and SDA pins to the correct pinouts on the Pi (and also power and ground) ... only these 4 wirings are needed

3. https://github.com/fm4dd/pi-bno055
4. Enable I2C on your Pi (Pi > Preferences > Raspberry Pi Configuration > Interfaces)  
5. Clone this repository. Follow instructions in README. Once you "make", the sensors should be calibrated
6. From there a command like "./getbno055 -t eul" will give orientation info (90deg test is working)
Make sure the mode (-m) has fusion set to ON. If not, execute command "./getbno055 -m ndof" and then you can get readings with "./getbno055 -t eul"
7. Once all of this is setup and functional, see imu_integrated_movement to see how to obtain IMU information from within another python script
