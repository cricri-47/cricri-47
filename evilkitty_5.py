from time import sleep
from os import stat
import json
import network
import socket

slider_2 = 17
response = ""
def file_exists(filename):
    try:
        return (stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False


    
def serve_page_1(page_name, modif):
    try:
        with open(page_name, "r") as f1:
            g1 = f1.read()
            #f1.close() {{analog_value}}
            g1 = g1.replace("50", str(modif))
            g1 = g1.replace("{{analog_value}}",str(modif))
            return g1
    except:
        return "Page 1 not found"

def serve_page_2(page_name, modif):
    try:
        with open(page_name, "r") as f1:
            g1 = f1.read()
            #f1.close()
            #g3 = g3.replace("{{slider_value}}",slider_value)
            return g1
    except:
        return "Page not found"

def serve_page_3(page_name, modif):
    try:
        with open(page_name, "r") as f1:
            g1 = f1.read()
            #f1.close()
            g1 = g1.replace("{{slider_value}}", str(modif))
            return g1
    except:
        return "Page 3 not found"

def serve_page_c(page_name, c_r, c_g, c_b):
    try:
        with open(page_name, "r") as f1:
            g1 = f1.read()
            #f1.close()
            g1 = g1.replace('value="50" class="slider" id="col_r"', 'value="'+str(c_r)+'" class="slider" id="col_r"')
            g1 = g1.replace('value="50" class="slider1" id="col_g"', 'value="'+str(c_g)+'" class="slider1" id="col_g"')
            g1 = g1.replace('value="50" class="slider2" id="col_b"', 'value="'+str(c_b)+'" class="slider2" id="col_b"')
            return g1
    except:
        return "Page_c not found"

ssid = "bureau 2.4G"
password = "erwannetpicasso"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

f1=''
f2=''
vitesse=''
jolie=''
nombre=''
Col_R = 0
Col_G = 0
Col_B = 0

with open("data.ini", "r") as f1:
    f2 = f1.read()
    print ('texte', f2)
    Col_R = int(f2.split("Col_R:")[1].split(",")[0])
    Col_G = int(f2.split("Col_G:")[1].split(",")[0])
    Col_B = int(f2.split("Col_B:")[1].split(",")[0])
    vitesse=f2.split("Vitesse:")[1].split(",")[0]
    jolie=f2.split("Jolie:")[1].split(",")[0]
    nombre=f2.split("Nombre:")[1].split(",")[0]
    print (vitesse,jolie,nombre)
    print (Col_R,Col_G,Col_B)
    f1.close()

slider_2 = vitesse
    

while True:
    #global slider_1
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print(request)
        
        if "/slider?" in request:              
            slider_2 = request.split("/slider?")[1].split(" ")[0]  # Extraire la valeur du curseur de la requête
            slider_2 = int(slider_2) if slider_2.isdigit() else slider_2  # Mettre à jour la valeur
            vitesse = str(slider_2)
            print ("/ Get Slider page 1",slider_2)
            #cl.send('image/gif')
        if "/slider_r?" in request:              
            slider_3 = request.split("/slider_r?")[1].split(" ")[0]  # Extraire la valeur du curseur de la requête
            slider_3 = int(slider_3) if slider_3.isdigit() else slider_3  # Mettre à jour la valeur
            Col_R = slider_3
            print ("/ Get Slider_R",Col_R)
            #cl.send('image/gif')
        if "/slider_g?" in request:              
            slider_4 = request.split("/slider_g?")[1].split(" ")[0]  # Extraire la valeur du curseur de la requête
            slider_4 = int(slider_4) if slider_4.isdigit() else slider_4  # Mettre à jour la valeur
            Col_G = slider_4
            print ("/ Get Slider_G",Col_G)
            #cl.send('image/gif')
            
        if "/slider_b?" in request:              
            slider_5 = request.split("/slider_b?")[1].split(" ")[0]  # Extraire la valeur du curseur de la requête
            slider_5 = int(slider_5) if slider_5.isdigit() else slider_5  # Mettre à jour la valeur
            Col_B = slider_5
            print ("/ Get Slider_B",Col_B)
            #cl.send('image/gif')
            
        if "GET /page1.html" in request:
            response = serve_page_1("page1.html", slider_2)
            #print (param_1)
            print ("/ Get page 1")
            request = ""
        if "GET /page2.html" in request:
            response = serve_page_c("page2.html", Col_R, Col_G, Col_B)
            #print (param_1)
            print ("/ Get page 2")
            request = ""    
        if "GET /page3.html" in request:
            response = serve_page_3("page3.html", slider_2)
            #print (param_1)
            print ("/ Get page 1")
            request = ""
        if "GET /?led=off" in request:
            with open('data.ini', "w") as f3:
                f = "\Lights\ \n"
                f = f + "Col_R:" + str(Col_R) + ",\n"
                f = f + "Col_G:" + str(Col_G) + ",\n"
                f = f + "Col_B:" + str(Col_B) + ",\n"
                f = f + "Vitesse:" + vitesse + ",\n"
                f = f + "Jolie:" + jolie + ",\n"
                f = f + "Nombre:" + nombre + ",\n"
                
                print(f)
                f3.write(f)
                f3.close()
            response = serve_page_2("index.html", slider_2)
            #print (param_1)
            print ("/ Get page 1")
            request = ""
            
        request=request.split("\\r\\n")[0].split(' ')
        #print(request)    
            
        if len(request) > 0:
            if request[0]=="b'GET":
                if request[1] == "/":
                    request[1] = "/index.html"
                print('file=',request[1])

                file= request[1]
                
                if file_exists(file):
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: ')
                    if request[1].find('.html') > 0:
                        cl.send('text/html')
                    elif request[1].find('.css') > 0:
                        cl.send('text/css')
                    elif request[1].find('.js') > 0:
                        cl.send('application/javascript')
                    elif request[1].find('.gif') > 0:
                        cl.send('image/gif')
                    elif request[1].find('.png') > 0:
                        cl.send('image/png')
                    elif request[1].find('.jpg') > 0:
                        cl.send('image/jpeg')
                    elif request[1].find('.gif') > 0:
                        cl.send('image/gif')
                   
                    else:
                        print('Not Implemented')
                    cl.send('\r\n\r\n')

                    file= request[1]
                    print(file,":",file_exists(file))
                    try:
                        with open(file, 'rb') as f:
                            while True:
                                c = f.read(1024)
                                if len(c) == 0:
                                    break
                                # print(cnt, c)
                                cl.sendall(c)
                    except Exception as e:
                        print("error", e)
                else:
                    cl.send('HTTP/1.0 404 OK\r\nContent-type: ')
                    cl.send('text/html\r\n\r\n<html><body>404 File not found</body></html>')
            elif request[0]=="b'POST":
                print('Not Implemented: todo')
        
        if len (response) > 0:
            cl.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
            response = ""
            #print (response)  
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')