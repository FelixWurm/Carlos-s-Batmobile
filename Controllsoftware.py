#Controllsoftware to controll one ore mor Calros Roboters


from logging import exception
import socket
from time import sleep as sl
from typing import Counter
from unittest import skip
import struct
import sys
import select
import serial
    
    
def serial_connect(device_name):
    ser = serial.Serial(device_name,115200,timeout = 0.1)
    return ser



serial_x = 0
serial_y = 0
serial_select_rover = 0;

serial_port = 0

def serial_read(current_device, devices,ser):
    cash = ser.readline()
    if cash:
        cash = cash.decode()
        end = len(cash)-1
        if cash[0] == 'Y':
            
            serial_y = decode_number(cash)
            print(serial_y)
        
        if cash[0] == 'X':
            serial_x = decode_number(cash)
            
        if cash[0] == 'T':
            next_device(current_device, devices)
            
    
def decode_number(number: str):
    print("+", number[1:])
    mynum = int(number[1:])
    print(type(mynum), mynum)
    
    
    if number[1] == "-":
        if number[3] != "\r":
            return (int(number[2])*10)+int(number[3])
        else:
            return number[2]
    
    else:
        if number[2] != "\r":
            return (int(number[1])*10)+ int(number[2])
        else:
            return number[1]


msg_dict = {
    "STAY_ALLIVE" : int(0),
    "DV_STRATE" : int(1),
    "DV_ROTAT" : int(2)
}


msg_udp_dict = {
    "READY_CON" : int(64),
    "ERROR" : int(128)
}



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


def connect(ip_addr, ip_port):
    print("Trying to connect to IP:", ip_addr,"  Port:", ip_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    Counter = 0
    while True:
        try:
            sock.connect((ip_addr, ip_port))
            return sock
        except Exception as e:
            print("Faild to connect to server!.... Retrying")
            print(str(e))
            sl(1)

        Counter = Counter +1
        if Counter > 3:
            print("FAILD to connect after 3 atemts. Exiting Programm")
            exit()
            
    sock.setblocking(0)
    print("Connection establoshed!")




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


def decode(msg,soc):
    pass


def connect_new_clinet(last_ip):
    if(last_ip != "0.0.0.0"):
        print("Please enter a IP adress you wish to connect to:")
        ip_addr = input()
        print("please enter a port:")
        ip_port = input()
        
    else:
        ip_addr = last_ip
        ip_port = 50000

    try:
        ip_port = int(ip_port)
    except:
        print("Faild to reed in Port, please only use Numbers")
        exit()
    
    try:
        soc = connect(ip_addr, ip_port)
    except:
        print


def setup_auto_discovery(port):
    udp_soc = socket.socket(socket.SOCK_DGRAM, socket.AF_INET)
    udp_soc.bind(("", port))
    udp_soc.setblocking(0)
    return udp_soc
    


def auto_discovery(udp_soc):
    ready = select.select([udp_soc],[],[],0)
    if ready[0]:
        msg, addr = udp_soc.recvfrom(1024)
        if msg[0] == msg_udp_dict["READY_CON"]:
            return addr
        
    return False
        
def next_device(cuurent_device, devices):
    if devices[cuurent_device +1]:
        return cuurent_device +1
    else:
        return 0

devices = []


def main():
    
    print("Welcome to the ideal Roboter controll Center")

    print(get_local_ip(), "<< Local IP")
    
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
        
        
        #auto discovery
        cash =  auto_discovery(udp_soc)
        
        if cash:
            print("Found new Device!  IP:", cash)
            print("To add IP to list off connectet devices type C without any argumenst")
            last_ip = cash
            
        
        #TCP conection handeling
        for soc in devices:
            ready = select.select([soc],[],[],0)
            if ready[0]:
                msg = soc.recv(2048)
                decode(msg,soc)
            
            
        #read out the Keyboard
        ready = select.select([sys.stdin],[],[],0)
        if ready[0]:
            cash = sys.stdin.readline().rstrip()
            if cash:
                if(cash[0] == "D"):
                    position = 1
                    try:
                        speed = finde_number(cash, position)
                        distance = finde_number(cash, position)
                    except:
                        print("Invalid Input")
                    cash = struct.pack("!Bff", int(1), speed, distance)
                    soc.sendall(cash)
                    
                if cash[0] == "R": 
                    pass


                if(cash[0] == "H"):
                    #print out a small Help promt:
                    help("gerneal")
                
                if(cash[0] == "C"):
                    connect_new_clinet(last_ip)
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
                    
                    



    soc.close()


d = []
d.append(2)


main()

#print(finde_number("D  67876.98  fwwes", 0))

