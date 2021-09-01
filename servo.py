#sudo pigpiod
import pigpio
import time

SERVO1_PIN = 19 # pitch
SERVO2_PIN = 18 # yaw

pi = pigpio.pi() # accesses the local Pi's GPIO

# flag used to stop the thread which controls the servo
stopFlag = False

def init_servo():
  # pin as output
  pi.set_mode(SERVO1_PIN, pigpio.OUTPUT)
  pi.set_mode(SERVO2_PIN, pigpio.OUTPUT)

  # set servo at 90 degree
  pi.set_servo_pulsewidth(SERVO1_PIN, 1500)
  pi.set_servo_pulsewidth(SERVO2_PIN, 1500)

def stop_servo():
  pi.set_servo_pulsewidth(SERVO1_PIN, 0)
  pi.set_servo_pulsewidth(SERVO2_PIN, 0)

def set(servo, value):
  if servo == "pitch":
    pi.set_servo_pulsewidth(SERVO1_PIN, value)
  elif servo == "yaw":
    pi.set_servo_pulsewidth(SERVO2_PIN, value)
  time.sleep(0.5)

def spin(pin_servo, time_delay):
    global stopFlag
    lim_low = 1200
    lim_high = 1800
    
    i = lim_low

    while not stopFlag:
      start = time.time()
      # move servo from left to right
      for i in range(0, lim_high - lim_low, 10):
        # set servo
        pi.set_servo_pulsewidth(pin_servo, i + lim_low)

        # sleep only if we aren't late
        to_sleep = start + i * time_delay - time.time()
        if to_sleep > 0:
          time.sleep(to_sleep)
              
      start = time.time()
      # move servo from right to left
      for i in range(0, lim_high - lim_low, 10):
        # set servo
        pi.set_servo_pulsewidth(pin_servo, lim_high - i)

        # sleep only if we aren't late
        to_sleep = start + i * time_delay - time.time()
        if to_sleep > 0:
          time.sleep(to_sleep)

    #period = time.time() - start_time
    #angle_speed = 40 / period * 2
    #print(period, angle_speed)

def spin_exe(time_delay):
  spin(SERVO2_PIN, time_delay) # yaw
  
