#Controllsoftware to controll one ore mor Calros Roboters


from distutils.debug import DEBUG
from ipaddress import ip_address
from logging import exception

#TCP and UDP conection
import socket

#Timing
from time import sleep as sl
import time


#from typing import Counter
#from unittest import skip

#struct to decode TCP packets
import struct

#waiting system
import sys
import select

#Serial connection to the Joistick
import serial

import dict



#Debug enable:
DEBUG = False



#Auto Discovery
AUTO_DISCOVERY = True

def serial_connect(device_name):
    ser = serial.Serial(device_name,115200,timeout = 0.1)
    return ser


class device_maneger:
    def __init__(self, ip,port,connect = False):
        self.last_keepalive = time.time()
        self.ip_addr = ip
        self.ip_port = port
        self.last_conn = 0
        
        if connect:
            return self.connect()
        else:
            return True
            
    def connect(self):
        print("Trying to connect to IP:", self.ip_addr,"  Port:", self.ip_port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        Counter = 0
        while True:
            try:
                self.sock.sendto(dict.msg_dict["CONN_REQUEST"],(self.ip_addr, self.ip_port))
                self.sock.setblocking(1)
                self.sock.settimeout(100)
                data = self.sock.recvfrom(1024)
                if(data[0] == dict.msg_dict["CONN_ACCEPT"]):
                    pass
                else:
                    raise Exception("Error no response from server. Is the ip correct?")
                self.last_comm = time.clock_gettime_ns()

                break
            except Exception as e:
                print("Faild to connect to server!.... Retrying")
                print(str(e))
                sl(1)

            Counter = Counter +1
            if Counter > 3:
                print("FAILD to connect after 4 atemts. Exiting Programm")
                return False
            
        self.sock.setblocking(0)
        print("Connection establoshed!")
        return True
    
    
    
    def send_data(self,msg):
        counter = 0
        while True:
            try:
                self.sock.sendto(msg)
                self.last_conn = time.time()
                return True
            except:
                if DEBUG:
                    print("Faild to send data, Retrying...")
                counter+1
                
                if(counter > 3):
                    if DEBUG:
                        print("Faild to connect after the 5th atempt")
                    return False
                    
    def send_keepalive(self):
        #sends if nesesary a keepalive signal. if the last communication is les then two seconds ago, do nothing
        if(self.last_comm -time.time() < -2):
            self.send_data(dict.msg_dict["KEEP_ALIVE"])
    

    def set_keepalive(self):
        self.last_comm = time.time()



serial_x = 0
serial_y = 0
serial_Button = False
new_set = [False, False]

serial_select_rover = 0;

serial_port = 0

def serial_read(current_device, devices,ser):
    global serial_x
    global serial_y
    global serial_Button
    try:
        cash = ser.readline()
    except:
        print("Error trying to reed from device")
        return False
        
    if cash:
        cash = cash.decode()
        end = len(cash)-1
        #speed
        if cash[0] == 'Y':
            serial_y = decode_number(cash)
            new_set[0] = True
        #direction
        if cash[0] == 'X':
            serial_x = decode_number(cash)
            new_set[1] = True
        if cash[0] == 'T':
            serial_Button = True
    return True
            
    
def decode_number(number: str):
    mynum = int(number[1:])
    return mynum


def get_local_ip():
    """Try to determine the local IP address of the machine."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use DNS server to determine own IP
        sock.connect(('8.8.4.4', 80))
        return sock.getsockname()[0]
    except socket.error:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'
    finally:
        sock.close() 




def help(typeofhelp):
    print("----------------------------------HELP--------------------------------------")
    print("commands:")
    print("D drive strate, needs speed and distance")
    print("d drive strate, needs speed and time")
    print("R rotate, needs angle and speed")


def decode(msg, soc, adress, port):
    print("incomming message Detectet!")

#returns True if it contains a number
def number(number_):

    if ((number_ == "1") or (number_ == "2") or (number_ == "3") or (number_ == "4") or (number_ == "5") or (number_ == "6") or (number_ == "7") or (number_ == "8") or (number_ == "9") or (number_ == "0")):
        return True
    else:
        if(number_ == "."):
            return True

    return False 


#functions that findes a number and fives it back as a float
def finde_number(input, position):
    first_number_found = False
    output = ""
    while True:
        if number(input[position]):
            output += input[position]
            position = position +1
            first_number_found = True
        else:
            if first_number_found == False:
                position = position +1
            else:
                break
    
    try:
        output = float(output)
    except:
        print("Faild to convert")
        return 0
    return output




def connect_new_clinet(last_ip):
    if(last_ip == "0.0.0.0"):
        print("Please enter a IP adress you wish to connect to:")
        ip_addr = input()
        print("please enter a UDP port:")
        ip_port = input()
        
    else:
        ip_addr = last_ip[0]
        ip_port = 50000

    try:
        ip_port = int(ip_port)
    except:
        print("Faild to reed in Port, please only use Numbers")
        exit()
    
    new_device = device_maneger(ip_addr, ip_port, False)
    
    if new_device.connect():
        print("Device conectet Sucsesfully")
        return new_device
    else:
        print("Faild to connect Device")



def setup_auto_discovery(port):
    udp_soc = socket.socket(socket.SOCK_DGRAM, socket.AF_INET)
    udp_soc.bind(("", port))
    udp_soc.setblocking(0)
    return udp_soc
    


def auto_discovery(udp_soc):
    ready = select.select([udp_soc],[],[],0)
    if ready[0]:
        msg, addr = udp_soc.recvfrom(1024)
        if msg[0] == dict.msg_dict["READY_CON"]:
            return addr
        
    return False


        
def next_device(current_device, devices):
    try:
        if devices[current_device +1]:
            return current_device +1
        print("Device changed to:", current_device)
    
    except:
        current_device = 0
        print("Device changed to:", 0)
        return 0

#list off sochets to all the connectet devices
devices = []
            


def main():
    
    #Values for seriell Stuff
    global serial_x
    global serial_y
    global serial_Button
    global new_set
    
    time_last_update = 0
    serial_selectet_device = 0
    console_select_device = 0
    
    #Programm Start, print some info
    print("Welcome to the ideal Roboter controll Center")
    print(get_local_ip(), "<< Local IP")
    
    if AUTO_DISCOVERY:
        udp_soc = setup_auto_discovery(25565)
    
    #save the last found ip to make connection easy
    last_ip = "0.0.0.0"
    
    #Serial suff
    serial_enable = False
    current_serial_device = 0


    #Main Loop
    while(True):
        #Serial controller stuff
        if serial_enable:
            serial_read(current_serial_device, devices,serial_port)
            
            if serial_Button:    
                next_device(serial_selectet_device,devices)
                serial_Button == False
                

        
            #if there is new data from the Joystick
            if(new_set[0] and new_set[1]):
                speed_a = serial_y
                speed_b = serial_y
                if serial_y == 0:
                    serial_x = serial_x * 0.6
                   
                    speed_a = serial_x
                    if(speed_a < 0):
                        speed_a -40
                    else:
                        speed_a +40
                        
                    speed_b = serial_x
                    if(speed_b < 40):
                        speed_b-40
                    
                    
                    
                else:
                    if(serial_x < 0):
                        serial_x = serial_x *(-1)
                        speed_b = speed_b - (serial_x * ((serial_y - 40) / 100))
                    else:
                        speed_a = speed_a - (serial_x * ((serial_y - 40) / 100))
                
            
                new_set = [False, False]
                msg = struct.pack("Bff", dict.msg_dict["DV_RAW_MODE"],speed_a,speed_b)
                
                
                devices[current_serial_device].sendall(msg)

        #end Serial Stuff
         
         
        #keep alive 
        for device in devices:
            device.send_keepalive()
        
        
        #auto discovery
        if AUTO_DISCOVERY:
            cash =  auto_discovery(udp_soc)
        
            if cash:
                print("Found new Device!  IP:", cash)
                print("To add IP to list off connectet devices type C without any argumenst")
                last_ip = cash
            
        
        #UDP conection handeling
        for device in devices:
            ready = select.select([device.sock],[],[],0)
            if ready[0]:
                msg = device.sock.recv(1024)
                if msg:
                    if msg[0] == dict.msg_dict["STAY_ALLIVE"]:
                        device.set_keepalive(time.time())
                        
        #send out keep alive signal eery two minuits
        
        
        #check if the all conecet nods are still present
        
            
        #read out the Keyboard
        ready = select.select([sys.stdin],[],[],0)
        if ready[0]:
            cash = sys.stdin.readline().rstrip()
            if cash:
                #Drive vorwards
                if(cash[0] == "D"):
                    position = 1
                    try:
                        speed = finde_number(cash, position)
                    except:
                        print("Invalid Input")
                    cash = struct.pack("!Bf", dict.DV_STRAIGHT, speed)
                    devices[console_select_device].send(cash)
                    

                #Rotate
                if cash[0] == "R":
                    pass


                if(cash[0] == "D"):
                    position = 1
                    try:
                        speed = finde_number(cash, position)
                    except:
                        print("Invalid Input")
                    cash = struct.pack("!Bf", int(1), speed)
                    devices[console_select_device].send(cash)


                #cal Mode
                if cash[0] == "T":
                    try:
                        speed = finde_number(cash, position)
                        time_ = finde_number(cash, position)
                    except:
                        print("Invalid Input")

                    cash = struct.pack("!Bf", dict.msg_dict["DV_STRAIGHT"], speed)
                    devices[console_select_device].send(cash)
                    sl(time_)
                    cash = struct.pack("!Bf", dict.msg_dict["DV_STOP"], speed)
                    devices[console_select_device].send(cash)                   


                #Drive in reverse
                if cash[0] == "R": 
                    pass

                #print out a small Help promt:
                if(cash[0] == "H"):
                    help("gerneal")
                
                if(cash[0] == "C"):
                    devices.append(connect_new_clinet(last_ip))
                    last_ip = ".0.0.0.0"
                
                if(cash[0] == "Y"):
                    print("connect a new Joystick to the USB port! Then enter the location of the port")
                    print("input s for standart port")
                    while True:
                        port = input()
                        if port:
                            break
                    if port == "s":
                        serial_enable = True
                        serial_port = serial_connect("/dev/ttyACM0")
                    else:
                        serial_enable = True
                        serial_port = serial_connect(port)
                        
                    print("connected!")
                    
                    


main()

#print(finde_number("D  67876.98  fwwes", 0))

