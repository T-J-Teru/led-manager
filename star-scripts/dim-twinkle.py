from star import Star
from time import sleep

# WIP: Would like to have dim, twinkling LEDs.

star = Star(pwm=True, initial_value=0.1)

try:
    leds = star.leds
    while True:
        for led in leds:
            led.pulse()
            sleep(.2)
except KeyboardInterrupt:
    star.close()
