from DWMTag import DWMTag

#Initialize the tag. This opens up the serial connection and issues commands to
#setup for reading the position
myTag = DWMTag()

for i in range(20):
    #call get_pos()
    position = myTag.get_pos()
    print(position)

#Close the serial connection
myTag.close_serial()
