# MQTT library van https://github.com/bborncr/ESP32MQTT-Micropython
# aangepast door Bns

#%% publish/subscribe thread
import esp32
import time
import _thread

start_time = time.ticks_ms()
interval = 10000 # 10 second interval for publishing data

# Returns True if interval has passed
def ready_to_publish():
    global start_time
    if time.ticks_ms() - start_time > interval:
        start_time = time.ticks_ms()
        return True
    else:
        return False

def pubsub():
    count = 1
    while True:
        checkwifi()                                                         # check if WiFi is still connected
        client.check_msg()                                                  # check for incoming messages (non-blocking)
        if ready_to_publish():                                              # if the interval time has passed, publish again
            temperature=esp32.raw_temperature()                             # get internal temperature of chip
            msg = '{"Count":%u,"Temperature":%2.2f}' % (count,temperature)  # create a message in JSON format
            client.publish('ESP32' + '/data/json', msg)
            count = count + 1

# launch pub/sub thread individually
_thread.start_new_thread(pubsub, ())

import time
import machine
from servo import Servo
from machine import Pin, ADC
from time import sleep



motion = False

def handle_interrupt(pin):  #Avoid using print() inside isr
  global motion
  motion = True
  global int_pin
  int_pin = pin

pir = Pin(14, Pin.IN, Pin.PULL_DOWN)
pir.irq(trigger = Pin.IRQ_RISING, handler = handle_interrupt)

servo_pin = machine.Pin(27)
my_servo = Servo(servo_pin)
delay = 0.01
min = 1
max = 90

LDR = ADC(Pin(33))
LDR.atten(ADC.ATTN_11DB)
led = Pin(26, Pin.OUT)
while True:
    LDR_value = LDR.read()
    if LDR_value < 1750:
        led.value(1)
    else: 
        led.value(0)
    print(LDR_value)
    sleep(0.25) 
    
    print(pir.value())
    time.sleep_ms(400)
    if motion:
        for i in range(min,max):
            my_servo.write_angle(i)
            time.sleep(delay)
        for i in range(max, min, -1):
            my_servo.write_angle(i)
            time.sleep(delay)
   


