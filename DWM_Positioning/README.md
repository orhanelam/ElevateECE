# DWM1001 Positioning System

## Files

* DWMTag.py: Class that defines the Tag object. Initializing the tag opens the serial connection and issues commands to begin reading the position of the Tag. Remaining methods are used to update the stored position, get the position, and close the serial connection.

* DWM1001_apicommands.py: Contains the commands listed in the DWM1001 api guide in a convenient place so that they are ready to be used in any program.

* TagClassTest.py: A simple test that initializes an instance of DWMTag, and demonstrates how to use the class methods to obtain position readings from the Tag.


## How to Run

Prerequisites: 
* A properly configured network of DWM1001s, with all anchors powered on. See https://www.decawave.com/wp-content/uploads/2019/03/DWM1001_Gateway_Quick_Deployment_Guide.pdf
* pyserial library (install by running 'pip install pyserial')
* While this code is compatible with both Python 2 and 3, we recommend using Python 3

1) Plug the DWM1001 dev board configured as the Tag into the USB port of the Raspberry Pi (or pc).
2) Find the port name for the device. On the pi, this can be done by running 'dmesg' in terminal. On a Mac, run 'python -m serial.tools.list_ports -v'
3) Run TagClassTest, specifying port_name when the tag is initialized.
4) The tag should connect and successfully print 200 position readings before closing the serial connection.

# Suggestions

For multithreading, call Tag.update_position() in a while loop. This continuously updates Tag.x_position, Tag.y_position and Tag.curr_time by reading the data coming in over the serial connection.

Only call Tag.get_pos() to get [Tag.x_position, Tag.y_position] which returns the values of Tag's instance variables.

## Links
For the complete guide to the DWM1001 API: https://www.decawave.com/sites/default/files/dwm1001-api-guide.pdf


