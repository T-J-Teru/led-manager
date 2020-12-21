from star import Star
from time import sleep

star = Star(pwm=True)
leds = star.leds
outer_range = range(1,26)

try:
    while True:
        for i in outer_range:
            leds[i].on()
            sleep(0.2)

        star.inner.blink(on_time=0.5,off_time=0.5,n=5,background=False)
        sleep(0.5)

        for i in outer_range:
            leds[i].off()
            sleep(0.2)

except KeyboardInterrupt:
    star.close()