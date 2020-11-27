#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


class l298n:
	def __init__(self, ena_pin, enb_pin, in1_pin, in2_pin, in3_pin, in4_pin):
		self.ena_pin = ena_pin
		self.enb_pin = enb_pin
		self.in1_pin = in1_pin
		self.in2_pin = in2_pin
		self.in3_pin = in3_pin
		self.in4_pin = in4_pin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.ena_pin, GPIO.OUT)
		GPIO.setup(self.enb_pin, GPIO.OUT)
		GPIO.setup(self.in1_pin, GPIO.OUT)
		GPIO.setup(self.in2_pin, GPIO.OUT)
		GPIO.setup(self.in3_pin, GPIO.OUT)
		GPIO.setup(self.in4_pin, GPIO.OUT)
		GPIO.output(self.in1_pin, GPIO.LOW)
		GPIO.output(self.in2_pin, GPIO.LOW)
		GPIO.output(self.in3_pin, GPIO.LOW)
		GPIO.output(self.in4_pin, GPIO.LOW)
		
	
		
	def pump1(self, speed, run_time):
		motor1 = GPIO.PWM(self.enb_pin, 1000)
		motor1.start(speed)
		motor2 = GPIO.PWM(self.ena_pin, 1000)
		motor2.start(speed)
		GPIO.output(self.in1_pin, GPIO.HIGH)
		GPIO.output(self.in3_pin, GPIO.LOW)
		GPIO.output(self.in2_pin, GPIO.LOW)
		GPIO.output(self.in4_pin, GPIO.LOW)
		time.sleep(run_time)
		
		
	def pump2(self, speed2, run_time2):
		motor1 = GPIO.PWM(self.enb_pin, 1000)
		motor1.start(speed2)
		motor2 = GPIO.PWM(self.ena_pin, 1000)
		motor2.start(speed2)
		GPIO.output(self.in1_pin, GPIO.LOW)
		GPIO.output(self.in3_pin, GPIO.HIGH)
		GPIO.output(self.in2_pin, GPIO.LOW)
		GPIO.output(self.in4_pin, GPIO.LOW)
		time.sleep(run_time2)
		
		
	def cleanup(self):
		GPIO.cleanup()





