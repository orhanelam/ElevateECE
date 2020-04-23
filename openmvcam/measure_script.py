3# AprilTags Test Measurements

import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)


# custom FOV settings

f_x = (16 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (16 / 2.952) * 120 # find_apriltags defaults to this if not set



#1.5cm wall offset

def degrees(radians):
    return (180 * radians) / math.pi

def z_cm(x):
    return (-1.3421*x + 1.3744)

def x_cm(x):
    return (-.9887*x - .046)





def z_cm(x):
    return (-3.315*x - 7.777)
   # return (-3.3122*x - 7.3831) rover level 16mm 10cm

#def z_cm(x):
    #return (-3.2388*x - 2.0373) #16mm 10cm


#def z_cm(x):
    #return (- 6.3603*x + 1.0597 - 10) #16mm 20cm

def near(x, base=10):
    return base * round(x/base)

win = []
angle = []
h = []
v = []
while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(families=image.TAG16H5, fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

        while(len(win) > 100):
            win.pop(0)
            angle.pop(0)
            h.pop(0)
            v.pop(0)

        win.append(round(tag.z_translation(), 3)) # this is highly variable, need to trim
        angle.append(degrees(tag.y_rotation()))
        h.append(tag.x_translation())
        v.append(tag.y_translation())

        temp = list(win)
        temp.sort()
        temp2 = list(angle)
        temp2.sort()
        temp3 = list(h)
        temp3.sort()
        temp4 = list(v)
        temp4.sort()


        if(len(temp) >= 100):
            #print_args = (temp3[4], temp4[4], temp[4],(temp[4] % 5) * 5, (temp[4] % 10) * 10, temp2[4])
            z = z_cm(temp[49])
            #z = temp[49]
            #print_args = (x_cm(temp3[4]), x_cm(temp4[4]), z_cm(temp[4]),temp2[4]) #converted
            print_args = (x_cm(temp3[4]), x_cm(temp4[4]), temp[4], z, near(z, 1), near(z, 3), near(z, 5), near(z, 10)) #converted
            # Translation units are unknown. Rotation units are in degrees.
            #print("Tx: %.1f, Ty %.1f, Tz %.1f, Ry %.1f" % print_args)
            #print("Tx: %.1f, Ty %.1f, Tz %.1f, T3 %.1f, T5 %.1f, T10 %.1f, Ry %.1f" % print_args)
            #print("Tx: %.1f, Ty %.1f, Unit %.1f, Tz %.1f, T1 %.1f, T3 %.1f, T5 %.1f, T10 %.1f" % print_args)
            print(near(z, .1))


