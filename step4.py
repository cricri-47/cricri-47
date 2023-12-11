# *** TMC2209 Test Program v0.1  tlfong01  2022jan02hkt1126 ***

# *** Import ***
from machine import Pin,PWM
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
pwm_fan = PWM(Pin(0, mode=Pin.OUT)) # Attach PWM object on the LED pin
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
   step2.high()
   #utime.sleep(0.01)
   time.sleep_us(3450)
   step2.low()
   time.sleep_us(3450)
   #utime.sleep(0.01)

def Zap(tour):
#     on part  bille exterieur, Rmax et on avance tout doux vers le centre
    direction1.high()
    direction2.low()
    t = 0
    while t < tour :
        enable2.low()
        enable1.low()
        x = 0
        mouv0=0
        u=0
        while x < 38400 :
            step1.high()
            time.sleep_us(500)
            step1.low()
            time.sleep_us(500)
            #x = x + 1
           
            mouv = math.sin(x/261)
            #print (mouv, mouv0)
            delta = (mouv-mouv0) * 150
            #print(delta, mouv0)
            if x > 383:
                u = (x % 384)
                if u-1 < 1:
                    direction2.low()
                    step2.high()
                    time.sleep_us(500)
                    step2.low()
                    time.sleep_us(500)
            direction2.high()
            #print ("YYY",y,delta)
            if delta > 0:
                direction2.low()
           
            if abs(delta) > 1:
                y = 0 
                while y < abs(delta):
                    step2.high()
                    time.sleep_us(500)
                    step2.low()
                    time.sleep_us(500)
                    y = y + 1
                   
                    mouv0 = mouv
            x = x + 1
        y = 0
        print("tour",t)
        while y < 2:
            direction2.low()
            step2.high()
            time.sleep_us(500)
            step2.low()
            time.sleep_us(500)
            y = y + 1
        t = t + 1
        #exit()
        
def superzap(tour):
#     on fait vibrer
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

       
t_debut = time.ticks_ms()# on note l'heure actuelle dans la variable t_debut
enable2.high()  
#Mot1(250,2000)
#Zap(39)
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
pwm_fan.duty_u16(0)
time.sleep(3)
enable2.high()
enable1.high()
pwm_fan.freq(4000)
#pwm_fan.duty_u16(15000)
time.sleep(3)
print ("zero ")
#time.sleep(3)
for duty in range(30_000,15000,-300):
    pwm_fan.duty_u16(duty) # For Pi Pico
    print("cycle",duty)
    time.sleep_ms(100)
#quit()
time.sleep_ms(1000)
#direction1.low()
x = 0
while x < 6981:
    #direction2.high()
    #print("x a pour valeur", x)
    #stepTwo()
    x = x + 1
enable1.low()
enable2.low()
totalbm1=0
totalbm2=0
bm1tot=0
bm2tot=0
dur=300


# Initialize SD card
sd = sdcard.SDCard(spi,cs)
 
# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")
# Create a file and write something to it
with open("/sd/test02.txt", "w") as file:
    file.write("Hello, SD World!\r\n")
    file.write("This is a test\r\n")
    file.write("second fichier\r\n")
print ("pret")
with open("carres1.txt", "r") as f1:
    init = 0
    theta0 = 0
    phi0 = 0
    ligne=0
    restbm1=0
    restbm2=0
    distance=0
    Ray0=0
    
    for line in f1:
        #var = line
        if "." in line[0:15] and len(line) > 1 and not "#" in line[0:5]:
        #if len(line) > 1 :
        
            ligne = ligne + 1
            theta = float(line.split()[0])
            Ray = float(line.split()[1])
            print("ligne :",ligne," theta :",theta," Ray :",Ray,"Ray0 :",Ray0)
            Phi = math.acos((Ray*Ray*4-2)/(2))
            thetac = math.acos(Ray) - theta 
            
            distance=(Ray0*Ray0+Ray*Ray-2*Ray0*Ray*math.cos(theta-theta0))
            distance =150* math.sqrt(abs(distance))
            print(" distance ",distance)
            theta = thetac
            Ray0=Ray

            if init == 1 :
                #print( " mot 1",theta,Phi,init,ligne)
                enable1.low()
                enable2.low() 
                direction1.low()

                direction2.low()
                bm1 = (theta - theta0) * (38400 / math.pi / 2) 
                totalbm1 = totalbm1 + abs(bm1)
                bm1 = bm1 #+ restbm1
                restbm1 = math.modf(bm1)[0]
                bm1 = math.modf(bm1)[1]
                
                bm2 = (Phi-phi0) * (13963.6363 /math.pi/2/0.51625) #+restbm2
                totalbm2 = totalbm2 + abs(bm2)
                bm2 = bm2 #+ restbm2
                restbm2 = math.modf(bm2)[0]
                bm2 = math.modf(bm2)[1]                
                #print(" bm1  " , bm1," rest_bm1  ",restbm1," bm2  " , bm2," restbm2  ",restbm2)
                
                if bm1 > 0 :
                    direction1.high()
                    
                
                if bm2 > 0 :
                    direction2.high()    
                
                phi0 = Phi
                theta0 = theta
               
                    
                if abs(bm1) > abs(bm2):
                    d = 0
                    if bm2 == 0 :
                        pas = abs(bm1*2)
                        d = abs(bm1)
                    if bm2 != 0 :
                        pas = abs(bm1/bm2)
                    z = 0
                    
                  
                    #print("step",str(pas))
                   
                       
                        
                       
                    
                    while z < abs(bm1) :
                        bm1tot = bm1tot + 1
                      
                        step1.high()
                        time.sleep_us(dur)
                      
                        step1.low()
                        time.sleep_us(dur)
                        
                       
                        if z // pas > d:
                        #print ("div")
                           step2.high()
                           time.sleep_us(dur)
                           step2.low()
                           time.sleep_us(dur)
                           d = z // pas
                           
                        z = z + 1
                        
                       
                            
    
                    #print ("reste 1  bm1",bm1, " bm2  ",bm2," pad  ",pas," d  ",d,"  reste ",restbm2,)
                    print ("reste 1  bm1",bm1, " bm1tot  ",bm1tot," pad  ",pas," d  ",d,"  reste ",restbm1)
                   
                
                if abs(bm2) > abs(bm1):
                    d = 0
                    if bm1 == 0 :
                        pas = abs(bm2*2)
                        d = abs(bm2)
                    if bm1 != 0 :
                        pas = abs(bm2/bm1)
                    x = 0
                    
                   
                    while x < abs(bm2) :
                        step2.high()
                        time.sleep_us(dur)
                        step2.low()
                        time.sleep_us(dur)
                        if x // pas > d:
                            step1.high()
                            time.sleep_us(dur)
                            step1.low()
                            time.sleep_us(dur)
                         
                            d = x // pas
                            
                        x = x + 1
                        #print("x:",x)
                 

                    print ("reste 2  bm1",bm1, " bm2  ",bm2," pad  ",pas," d  ",d,"  reste ",restbm2,)
                    x = 0

    
            if init == 0 :
                #print ( " mot 0",str(theta),str(Phi),init)
                theta0 = theta
                phi0 = Phi
                init = 1
           
               
    #print ("bm1 mesure :",bm1tot, "bm1 theorique :", totalbm1 )          
    
  #  l1=f1.readline()
  #  print(l1)
  #  l1=f1.readline()
   # print(l1)
    #f2 = f1.read()
    #print ('texte', f2)
    #Col_R = int(f2.split("Col_R:")[1].split(",")[0])
    #Col_G = int(f2.split("Col_G:")[1].split(",")[0])
    #Col_B = int(f2.split("Col_B:")[1].split(",")[0])
    #vitesse=f2.split("Vitesse:")[1].split(",")[0]
    #jolie=f2.split("Jolie:")[1].split(",")[0]
    #nombre=f2.split("Nombre:")[1].split(",")[0]
    #print (vitesse,jolie,nombre)
   # print (Col_R,Col_G,Col_B)
    f1.close()    
t_fin = time.ticks_ms()       # on note l'heure actuelle après l’exécution du programme dans la variable t_fin
print ("pertes",totalbm1, totalbm2)
duree = t_fin - t_debut  # calcul du temps écoulé en millisecondes
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