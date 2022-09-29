#Control-software to control one ore mor Calros robot

#for connection to outside
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

#Serial connection to the joystick
import serial

import dict


#Debug enable:
DEBUG = True



#Auto Discovery
AUTO_DISCOVERY = True

def serial_connect(device_name):
    ser = serial.Serial(device_name,115200,timeout = 0.1)
    return ser


class device_manager:
    def __init__(self, ip,port,connect = False):
        self.ip_addr = ip
        self.ip_port = port
        self.last_conn = 0
        
        if connect:
            if not self.connect():
                raise Exception("Could not connect!")
            
    def connect(self):
        print("Trying to connect to IP:", self.ip_addr,"  Port:", self.ip_port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        Counter = 0
        while True:
            try:
                self.sock.sendto(struct.pack("!B",dict.msg_dict["CONN_REQUEST"]),(self.ip_addr, self.ip_port))
                self.sock.setblocking(1)
                self.sock.settimeout(5)
                data , self.addr = self.sock.recvfrom(1024)
                print (data)
                if data[0] == dict.msg_dict["CONN_ACCEPT"]:
                    pass
                else:
                    raise Exception("Error wrong response from server. Is the ip correct?")
                self.last_comm = time.time_ns()

                break
            except Exception as e:
                print("Failed to connect to server!.... Retrying (", e, ")")
                sl(1)

            Counter = Counter +1
            if Counter > 3:
                print("Failed to connect after 4 attempts")
                return False
            
        self.sock.setblocking(0)
        print("Connection established!")
        return True
    
    
    
    def send_data(self,msg):
        counter = 0
        while True:
            try:   
                self.sock.setblocking(1)
                self.sock.sendto(msg,self.addr)
                self.sock.setblocking(0)
                self.last_conn = time.time_ns()
                return True
            except Exception as e:
                if DEBUG:
                    print("Failed to send data, Retrying... (",e,")")
                counter = counter + 1
                
                if(counter > 3):
                    if DEBUG:
                        print("Failed to connect after the 4th attempt")
                    return False

    #sends if necessary a keepalive signal. if the last communication is les then two seconds ago, do nothing
    def send_keepalive(self):
        if(self.last_comm -time.time_ns() < -2000000000):
            self.send_data(struct.pack("!B", dict.msg_dict["STAY_ALIVE"]))
            self.last_comm = time.time_ns()
    
    #an ACK for a keepalive is receive
    def set_keepalive(self):
        self.last_comm = time.time_ns()



serial_x = 0
serial_y = 0
serial_Button = False
new_set = [False, False]

serial_select_rover = 0

serial_port = 0

def serial_read(current_device, devices,ser):
    global serial_x
    global serial_y
    global serial_Button
    try:
        cache = ser.readline()
    except:
        print("Error trying to reed from device")
        return False
        
    if cache:
        cache = cache.decode()
        end = len(cache)-1
        #speed
        if cache[0] == 'Y':
            serial_y = decode_number(cache)
            new_set[0] = True
        #direction
        if cache[0] == 'X':
            serial_x = decode_number(cache)
            new_set[1] = True
        if cache[0] == 'T':
            serial_Button = True
    return True
            
    
def decode_number(number: str):
    my_num = int(number[1:])
    return my_num


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




def help(typeof_help):
    print("----------------------------------HELP--------------------------------------")
    print("commands:")
    print("D drive strate, needs speed and distance")
    print("d drive strate, needs speed and time")
    print("R rotate, needs angle and speed")



#returns True if it contains a number
def number(number_):

    if ((number_ == "1") or (number_ == "2") or (number_ == "3") or (number_ == "4") or (number_ == "5") or (number_ == "6") or (number_ == "7") or (number_ == "8") or (number_ == "9") or (number_ == "0") or (number_ == "-")):
        return True
    else:
        if(number_ == "."):
            return True

    return False 


#functions that finds a number and fives it back as a float
def find_number(input, position):
    first_number_found = False
    output = ""
    while True:
        try:
            if number(input[position]):
                output += input[position]
                position = position +1
                first_number_found = True
            else:
                if first_number_found == False:
                    position = position +1
                else:
                    break
        except IndexError:
            break        
    
    try:
        output = float(output)
    except:
        print("Failed to convert")
        return 0
    return output , position



def connect_new_client(last_ip):
    if(last_ip == "0.0.0.0"):
        print("Please enter a IP address you wish to connect to, or C1 to C5 for default Calos rover")
        ip_addr = input()
        if ip_addr[0] == "C":
            if ip_addr[1] == "1":
                ip_addr = "192.168.199.101"
                ip_port = 50000
            elif ip_addr[1] == "2":
                ip_addr = "192.168.199.102"
                ip_port = 50000
            elif ip_addr[1] == "3":
                ip_addr = "192.168.199.103"
                ip_port = 50000
            elif ip_addr[1] == "4":
                ip_addr = "192.168.199.104"
                ip_port = 50000
            elif ip_addr[1] == "5":
                ip_addr = "192.168.199.105"
                ip_port = 50000
            elif ip_addr[1] == "6":
                ip_addr = "192.168.199.106"
                ip_port = 50000
        else:
            print("please enter a UDP port:")
            ip_port = input()
        
    else:
        ip_addr = last_ip[0]
        ip_port = 50000

    try:
        ip_port = int(ip_port)
    except:
        print("Failed to reed in Port, please only use Numbers")
        exit()
    
    new_device = device_manager(ip_addr, ip_port, False)
    
    if new_device.connect():
        print("Device connected successful")
        return new_device
    else:
        print("Failed to connect Device")



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

#list off Sockets to all the connected devices
devices = []
            


def main():
    
    #Values for serial Stuff
    global serial_x
    global serial_y
    global serial_Button
    global new_set
    
    time_last_update = 0
    serial_selected_device = 0
    console_select_device = 0
    
    #Program Start, print some info
    print("Welcome to the ideal rover control Center")
    print(get_local_ip(), "<< Local IP")
    
    if AUTO_DISCOVERY:
        udp_soc = setup_auto_discovery(25565)
    
    #save the last found ip to make connection easy
    last_ip = "0.0.0.0"
    
    #Serial stuff
    serial_enable = False
    current_serial_device = 0

    serial_failed_counter = 0
    filename_ = File.open()
    #Main Loop
    while(True):
        #Serial controller stuff
        if serial_enable:
            if not serial_read(current_serial_device, devices,serial_port):
                serial_failed_counter = serial_failed_counter+1
            else:
                serial_failed_counter = 0

            if serial_failed_counter >20:
                serial_enable = False
            
            if serial_Button:    
                next_device(serial_selected_device,devices)
                serial_Button == False
                

        
            #if there is new data from the Joystick
            if new_set[0] and new_set[1]:
                if serial_x == 0:
                    speed_a = serial_y
                    speed_b = serial_y
                
                elif serial_y == 0:
                    speed_a = serial_x * 0.6
                    if speed_a < 0:
                        speed_a = speed_a -40
                    else:
                        speed_a = speed_a + 40

                    speed_b = (serial_x * 0.6) * (-1)
                    if speed_b < 0:
                        speed_b = speed_b -40
                    else:
                        speed_b = speed_b + 40  

                else:
                    #in case somebody wants to repair the Joystick, you need to add code here.
                    pass                  
            
                new_set = [False, False]
                msg = struct.pack("Bff", dict.msg_dict["DV_RAW_MODE"],speed_a,speed_b)
                
                
                devices[current_serial_device].send_data(msg)

        #end Serial Stuff
         
         
        #keep alive 
        for device in devices:
            if not device == None:
                device.send_keepalive()
        
        
        #auto discovery
        if AUTO_DISCOVERY:
            cache =  auto_discovery(udp_soc)
        
            if cache:
                print("Found new Device!  IP:", cache)
                print("To add IP to list off connect devices type C without any arguments")
                last_ip = cache
            
        
        #UDP connection handling
        for device in devices:
            ready = select.select([device.sock],[],[],0)
            if ready[0]:
                msg = device.sock.recv(1024)
                if msg:
                    if msg[0] == dict.msg_dict["STAY_ALIVE"]:
                        device.set_keepalive(time.time())

                    if msg[0] == dict.msg_dict["POS_CURRENT_RAW"]:
                        pos = struct.unpack("!Bdd", msg)
                        print("Position = ",pos[1] * 1," cm :",pos[2] * 1, " cm")

                    if msg[0] == dict.msg_dict["POS_CURR_LEFT"]:
                        pos = struct.unpack("!Bff", msg)
                        print("Position = ",pos[1] ," mm :",pos[2] , " cm")
                        
        #send out keep alive signal every two minutes
        
        
        #check if the all connected nods are still present
        
            
        #read out the Keyboard
        ready = select.select([sys.stdin],[],[],0)
        if ready[0]:
            cache = sys.stdin.readline().rstrip()
            if cache:
                #Drive forwards
                if(cache[0] == "D"):
                    position = 1
                    try:
                        speed = find_number(cache, position)
                    except:
                        print("Invalid Input")
                    cache = struct.pack("!Bf", dict.DV_STRAIGHT, speed)
                    devices[console_select_device].send_data(cache)
                    

                #Reset
                if cache[0] == "R":
                    cache = struct.pack("!B", dict.msg_dict["POS_RESET"])
                    devices[console_select_device].send_data(cache)                   


                if(cache[0] == "D"):
                    position = 1
                    try:
                        speed = find_number(cache, position)
                    except:
                        print("Invalid Input")
                    cache = struct.pack("!Bf", int(1), speed)
                    devices[console_select_device].send_data(cache)


                #cal Mode
                if cache[0] == "T":
                    if cache[1] == "S" or cache[1] == "D":
                        try:
                            position = 2
                            speed , position= find_number(cache, position)
                            time_  , position= find_number(cache, position)

                        except Exception as e:
                            print("Invalid Input (", e, ")")

                        cache = struct.pack("!Bff", dict.msg_dict["DV_CALL_STRAIGHT"], speed,time_)
                        devices[console_select_device].send_data(cache)
                 

                    if cache[1] == "R":
                        try:
                            position = 2
                            speed , position= find_number(cache, position)
                            time_ , position= find_number(cache, position)
                        except Exception as e:
                            print("Invalid Input (", e, ")")

                        cache = struct.pack("!Bff", dict.msg_dict["DV_CALL_ROTATE"], speed, time_)
                        devices[console_select_device].send_data(cache)


                #Drive in reverse
                if cache[0] == "R": 
                    pass

                #print out a small Help promt:
                if(cache[0] == "H"):
                    help("general")
                
                if(cache[0] == "C"):
                    cache_ = connect_new_client(last_ip)
                    if cache_:
                        devices.append(cache_)
                    last_ip = ".0.0.0.0"
                
                if(cache[0] == "Y"):
                    print("connect a new Joystick to the USB port! Then enter the location of the port")
                    print("input S for default port")
                    while True:
                        port = input()
                        if port:
                            break
                    if port == "S":
                        try:
                            serial_enable = True
                            serial_port = serial_connect("/dev/ttyACM0")
                            print("connected!")
                        except:
                            print("Could not connect to default port. check connection!")
                    else:
                        try:
                            serial_port = serial_connect(port)
                            serial_enable = True
                            print("connected!")
                        except Exception as e:
                            print("Could not connect Joystick (",e,")")
                        

                    
                    

if __name__ == "__main__":
    main()

