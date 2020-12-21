from time import sleep
from star import Star
    
step = 0.5
count = 0
star = Star(pwm=True)
leds = star.leds

length=4
start=0
end=start+length-1
on_brightness=1.0
off_brightness=0.0


try:
    while True: 
        leds[1].value=on_brightness                
        for x in range(25):
            if(x % length == start):
                leds[x+1].value=on_brightness 
            else:
                leds[x+1].value=off_brightness 
                         
        start=(start+1)%length

        sleep(0.2)

except KeyboardInterrupt:
    star.close()
