from DWMTag import DWMTag
'''
Initialize the tag. This opens up the serial connection and issues commands to
setup for reading the position
'''

myTag = DWMTag()
myTag.update_position()

'''
For multithreading I would suggest calling myTag.update_position in a while loop.
This continuously updates myTag.x_position, myTag.y_position and myTag.curr_time
by reading the data coming in over the serial connection.

Only call myTag.get_pos() to get [myTag.x_position, myTag.y_position]
'''

'''
Here I just sequentially call update_position() and get_pos()
'''
for i in range(200):
    #call get_pos()
    myTag.update_position()
    position = myTag.get_pos()
    print(position)

#Close the serial connection
myTag.close_serial()
