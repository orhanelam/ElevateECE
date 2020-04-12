import RPi.GPIO as GPIO
import time


class motorController:
	def __init():

		self.turnRatio = 1 #ratio of seconds per degree
		self.moveRation = 1 #ratio of seconds per meter

		# These are the pins for a 2B rasbperry pi, may differ for other models. 
		# https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=105044 to get 
		# pins.

		leftPin = 18
		rightPin = 12

		leftMotor = GPIO.PWM(leftPin,250)
		leftMotor.start(0)

		rightMotor = GPIO.PWM(rightPin, 250)
		rightMotor.start(0)



	def turn(left, degrees, speed)
			turnMotor(left, -speed)
			turnMotor(not left, speed)
			time.sleep(degrees * turnRatio * 100 / speed)
	
	def turnLeft(degrees, speed)
		turn(True, degrees, speed)

	def turnRight(False, degrees, speed)
		turn(False, degrees, speed)

	def move(meters, speed)
		turnMotor(True, speed)
		turnMotor(False, speed)
		time.sleep(meters * moveRatio * 100 / speed)


	#left: if true, set left motor, otherwise set right.
	# speedPercentage: -100 to 100, sets direction of motor and percent of max motor 	# rotation speed to turn at.
	def turnMotor(left, speedPercentage)
		if (speedPercentage > 100):
			speedPercentage = 100
		elif (speedPercentage < -100):
			speedPercentage = -100
		speed = 75 + -0.25 * speedPercentage
		if (left):
			leftMotor.ChangeDutyCycle(speed)
		else:
			rightMotor.ChangeDutyCycle(speed)


			