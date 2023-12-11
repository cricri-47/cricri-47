# *** TMC2209 Test Program v0.1  tlfong01  2022jan02hkt1126 ***

# *** Import ***
from machine import Pin, PWM
#import utime
import time
import math
#from os import stat
import os
import uos
import machine
import sdcard


# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(1, machine.Pin.OUT)
 
# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(4))
 
# Initialize SD card
sd = sdcard.SDCard(spi, cs)

direction1 = Pin(16, Pin.OUT)
step1 = Pin(17, Pin.OUT)
enable1 = Pin(15, Pin.OUT)
direction2 = Pin(12, Pin.OUT)
step2 = Pin(13, Pin.OUT)
enable2 = Pin(11, Pin.OUT)

enable1.low()
direction1.high()
enable2.low()
direction2.high()
def stepOne():
  step1.high()
  #utime.sleep(0.01)
  time.sleep_us(450)
  step1.low()
  time.sleep_us(450)
  #utime.sleep(0.01)
def stepTwo():
    enable2.low()
    direction2.low()
    step2.high()
   #utime.sleep(0.01)
    time.sleep_us(450)
    step2.low()
    time.sleep_us(450)
   #utime.sleep(0.01)
def superzap(tour):
#     on part  bille exterieur, Rmax et on avance tout doux vers le centre
    direction1.high()
    t = 0
    while t < tour :
        direction1.low()
        enable1.low()
        x = 0
        while x < 100 :
            step1.high()
            time.sleep_us(30)
            step1.low()
            time.sleep_us(200)
            x = x + 1
        direction1.high()
        x = 0
        while x < 100 :
            step1.high()
            time.sleep_us(30)
            step1.low()
            time.sleep_us(200)
            x = x + 1
        t=t+1
        x = 0
        while x < 3000 :
            step1.high()
            time.sleep_us(300)
            step1.low()
            time.sleep_us(200)
            x = x + 1
        t=t+1   


    
def Mot1(steps,duree):
    us_time = int (duree * 1000 / steps/2)
    print(us_time,steps/duree*1000)
    x = 0
    if us_time > 100 :
        while x <  steps:
            enable1.low()  
            time.sleep_us(us_time)
            step2.high()
            step1.high()
            time.sleep_us(us_time)
            step2.low()
            step1.low()
            time.sleep_us(us_time)
            y = 0
            while y < 5:
                step2.high()
                time.sleep_us(us_time)
                step2.low()
                time.sleep_us(us_time)
                y=y+1
            x = x + 1
            
    else:
        print("temps trop court")



pwm_fan = PWM(Pin(0, mode=Pin.OUT)) # Attach PWM object on the LED pin

# Settings

pwm_fan.duty_u16(0)
time.sleep(3)
enable2.high()
enable1.high()
pwm_fan.freq(4000)
#pwm_fan.duty_u16(15000)
time.sleep(3)
print ("zero ")
#time.sleep(3)
for duty in range(20_000,15000,-300):
    pwm_fan.duty_u16(duty) # For Pi Pico
    print("cycle",duty)
    time.sleep_ms(100)


t_debut = time.ticks_ms()# on note l'heure actuelle dans la variable t_debut
print ("reset ")
enable2.high()
enable1.high()
#Mot1(250,2000)
#Zap(23)
#exit()
time.sleep(5)

#superzap(20)
print("finfin")
time.sleep(1)
# ici les instructions du programme  
x = 0
enable1.low()
while x < 38400:
    direction1.low()
    #print("x a pour valeur", x)
    #stepOne()
    x = x + 1
print("fini")
enable1.high()
#exit()
enable2.low()
x=0
while x < 6981:
    #direction2.low()
    #stepTwo()
    #print("x a pour valeur", x)
    x=x + 1
print("fini")
enable2.high()
#quit()
time.sleep_ms(1000)
#direction1.low()
x = 0
while x < 6981:
    direction2.high()
    #print("x a pour valeur", x)
    #stepTwo()
    x = x + 1
enable1.low()
enable2.low()
dur = 450
totalbm1 =0
totalbm2=0

direction1.low() 
t=0
d=0
count=0

ligne=0
restbm1=0
restbm2=0

while count < 500:
    direction2.low() 
    z=0
    t=0
    d=0
    enable2.low()
    direction2.low()
    while z < 9000 :
        step1.high()
        time.sleep_us(dur)
        step1.low()
        time.sleep_us(dur)
        
        t=math.modf(z)[1]
        ligne = ligne+1
        #print (t,d)
        if t > d:
            step2.high()
            time.sleep_us(dur)
            step2.low()
            time.sleep_us(dur)
            #print (z,t)
            d = t
            totalbm2 = totalbm2+1
        z=z+1
    z=0
    t=0
    d=0
    direction2.high() 
    while z < 9000 :
        step1.high()
        time.sleep_us(dur)
        step1.low()
        time.sleep_us(dur)
        
        t=math.modf(z)[1]
        ligne = ligne+1
        #print (t,d)
        if t > d:
            step2.high()
            time.sleep_us(dur)
            step2.low()
            time.sleep_us(dur)
            #print (z,t)
            d = t
            totalbm2 = totalbm2+1
        z=z+1
    print ("count",count,"reste 2   bm2  ",totalbm2," pad   d  ",d, "z ",z,"  ligne ",ligne)
    count = count+1

 
t_fin = time.ticks_ms()       # on note l'heure actuelle après l’exécution du programme dans la variable t_fin
print ("pertes",totalbm1, totalbm2)
duree = (t_fin - t_debut)/1000  # calcul du temps écoulé en millisecondes

rpm = 60/duree*1000
cm = rpm/60
print(duree/1000,rpm,cm)
time.sleep(1)
direction1.high()
direction2.low()

time.sleep_ms(30)
t_debut = time.ticks_ms() 
#Mot1(166330,150000)
print(" durée :",(time.ticks_ms()-t_debut))

print("Fin")

enable1.high()  
enable2.high()     