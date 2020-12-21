from time import sleep
from star import Star
import datetime
    
step = 0.5
count = 0
star = Star(pwm=True)
leds = star.leds
dt = datetime.datetime.today()

length=25
if(dt.day < 25):
    length=dt.day
start=0
end=start+length-1
on_brightness=0.5
off_brightness=0.0


try:
    leds[0].pulse()
    while True:                
        dt = datetime.datetime.today()
        if(dt.day != length and dt.day <= 25):
            length=dt.day
        for y in range(25):
            x = y+1;
            if(end<start):
                if(x>=start or x<=end+1):
                    leds[x].value=on_brightness 
                else:
                    leds[x].value=off_brightness
            else:
                if(x>=start and x<=end):
                    leds[x].value=on_brightness
                else:
                    leds[x].value=off_brightness                           
        start=(start+1)%26
        end=(end+1)%26

        sleep(0.2)

except KeyboardInterrupt:
    star.close()
