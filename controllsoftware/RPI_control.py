# Script that runs on the RPi in order to control the movement and the Sensor data
import os
from pickletools import long4
import select, sys, struct
from turtle import distance
import RPi.GPIO as GPIO
from time import sleep as sl
import time
import socket
import dict
import subprocess
from dataclasses import dataclass

#Debug
DEBUG = True


#Objects to store the position values
@dataclass
class point:
    x : float = 0
    y : float = 0



@dataclass
class Move:
    start_position  : point
    end_position    : point
    direction       :int

    move_mode       : int = dict.msg_dict["NO_MODE"]
    move_speed      : int = 0
    move_start      : int = 0
    move_end        : int = 0



#Motor control Pin
left_fwd = 12
left_bwd = 26
right_fwd = 13
right_bwd = 19


udp_port = 25565
udp_addr = "169.254.2.1"



#Setup the GPIO stuff
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_fwd, GPIO.OUT)
GPIO.setup(right_fwd, GPIO.OUT)
GPIO.setup(left_bwd, GPIO.OUT)
GPIO.setup(right_bwd, GPIO.OUT)

#Setup some PWM stuff
pi_pwm_l = GPIO.PWM(left_fwd, 1000)
pi_pwm_l.start(0)

pi_pwm_r = GPIO.PWM(right_fwd, 1000)
pi_pwm_r.start(0)


pi_pwm_l_bwd = GPIO.PWM(left_bwd, 1000)
pi_pwm_l_bwd.start(0)

pi_pwm_r_bwd = GPIO.PWM(right_bwd, 1000)
pi_pwm_r_bwd.start(0)


#Drive...
class drive:
    def __init__(self):
        self.end_time = 0


    def drive (self, speed_l, speed_r, dv_time):
        #check for correct input
        if((0 < speed_l < 40)or (-40 < speed_l < 0)):
            print("incorrect Input speed_l, must be between -100 to -40 or 40 to 100" )
            return

        if((0 < speed_r < 40)or (-40 < speed_r < 0)):
            print("incorrect Input speed_r, must be between -100 to -40 or 40 to 100" )
            return

        set_motor_speed(speed_l, speed_r)
        self.end_time = time.time_ns() + (dv_time * 1000000000)

    def run(self):
        if self.end_time < time.time_ns() and self.end_time != 0:
            set_motor_speed(0,0)
            self.end_time = 0




def set_motor_speed(speed_l : int, speed_r :int):
    speed_l = value_check(speed_l)
    speed_r = value_check(speed_r)
    if speed_l == 0:
         pi_pwm_l.ChangeDutyCycle(0)
         pi_pwm_l_bwd.ChangeDutyCycle(0)
    else:
        if(speed_l > 0):
            pi_pwm_l.ChangeDutyCycle(speed_l)
            pi_pwm_l_bwd.ChangeDutyCycle(0)
        else:
            pi_pwm_l.ChangeDutyCycle(0)
            pi_pwm_l_bwd.ChangeDutyCycle(speed_l*(-1))

    if speed_r == 0:
        pi_pwm_r.ChangeDutyCycle(0)
        pi_pwm_r_bwd.ChangeDutyCycle(0) 
    else:
        if(speed_r > 0):
            pi_pwm_r.ChangeDutyCycle(speed_r)
            pi_pwm_r_bwd.ChangeDutyCycle(0)
        else:
            pi_pwm_r.ChangeDutyCycle(0)
            pi_pwm_r_bwd.ChangeDutyCycle(speed_r*(-1))    


def value_check(value):
    if(value > 100):
        print("value was to big! (",value, ")")
        value = 100
    elif value < -100:
        print ("Value was to small! (", value, ")")

    return value

def drive_ (speed, time):
    drive(speed, speed, time)



#speed in M at a given speed, from 100 to 40 in increments of 10
speed_distance = [0.23, 0.1975,0.18, 0.16, 0.1375, 0.12, 0.09]



#distance in M, speed in percent (0-100)
def drive_dst(speed, distance):
    cash = speed %10
    if(cash >= 5 ):
        speed_ = ((speed - cash) + 10) / 10
    else:
        speed_ = (speed - cash) /10
    time = distance / speed_distance[int(10-speed_)]
    drive_(speed, time)


def rotate(speed, time):
    if speed < 40 and speed > -40:
        return
    drive(speed, speed *(-1),time)


#Function to get your local ip address
def get_local_ip():
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


def udp_discovery_setup():
    return socket.socket(socket.SOCK_DGRAM, socket.AF_INET)



def udp_discovery(discovery_port, discovery_addres, udp_soc, msg):
    udp_soc.sendto(struct.pack("!B",msg),(discovery_addres, discovery_port))



class mv_observer:
    def __init__(self) -> None:
        #mode (strate, rotate since the last change)
        self.last_mode = dict.msg_dict["NO_MODE"]
        self.last_speed = 0
        self.last_mode_beginning = 0
        self.last_start_position = point(0,0)
        self.last_direction = 0

        self.list_of_moves = []

    
    def move(self,mode, speed):
        #lok if the mode has changed significantly, if so save the old move, and calculate start and end position.
        if not (mode == self.last_mode and speed == self.last_speed):
            #Filter out just start moving 
            if self.last_mode ==  dict.msg_dict["NO_MODE"]:
                #com from no move to some movement
                self.last_mode = mode
                self.last_speed = speed
                self.last_mode_beginning = time.time_ns()
            
            else:
                #there was some change, so there needs to by an event appended

                #save the current data
                cash_move = Move
                cash_move.move_speed = self.last_speed
                cash_move.move_type = self.last_mode
                cash_move.move_start = self.last_mode_beginning
                cash_move.start_position = self.last_start_position


                cash_move.move_end = time.time_ns()

                self.list_of_moves.append(cash_move)

                #save the new last set data
                self.last_mode = mode
                self.last_speed = speed
                self.last_mode_beginning = time.time_ns()   

    def cal_end_position(self, move = Move):
        if move.move_mode == dict.msg_dict["NO_MODE"]:return

        if move.move_mode == dict.msg_dict["DV_STRATE"]:
            pass
            #Calculate passed time, than use that to calculate the Distance (influenced by the speed), then calculate a new point
        if move.move_mode == dict.msg_dict["DV_ROTATE"]:
            pass






#UDP
def UDP_setup():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Bind Server to localhost
    soc.bind(("", 50000))

    return soc

def udp_connect(soc = socket.socket):
    counter = 0
    while True:
        data, addr= soc.recvfrom(1024)
        if data[0] == dict.msg_dict["CONN_REQUEST"]:
            soc.sendto(struct.pack("!B", dict.msg_dict["CONN_ACCEPT"]), addr)
            soc.setblocking(0)
            return addr
        else:
            counter = counter +1
            print("connection attempt with invalid init sequence, open for retrys : ", counter)
            soc.sendto(struct.pack("!B",dict.msg_dict["ERROR_CONN"]), addr)


#converts a number from -100 to 100 toto -100-40, 40-100
def convert_to_motor(input):
    input  = input* 0.6
    if(input < 0):
        input = input -40
    else:
        input = input +40

    return input



def calculate_position(mode, time, speed, last_position):
    if mode == "R":
        pass
    if mode == "D":
        pass


def main():    
    #setup the TCP server
    soc = UDP_setup()
    
    print("IP:", get_local_ip())
    
    #send discovery signal once, should by send every minuit, nonblocking server requiert.
    udp_soc = udp_discovery_setup()
    udp_discovery(udp_port, udp_addr, udp_soc,dict.msg_dict["READY_CONN"])
    
    #try to connect to a UDP Host:
    ip_addr = udp_connect(soc)   
    
    print("Connected to:", ip_addr)
    
    
    last_update = time.time_ns()
      

    #Idee: Nach jeder veränderung der Geschwindigkeit Die Position neu bestimmen

    #init drive class
    Drive = drive()

    while True:
        Drive.run()

        #stop the motor in case of bad connection      
        #1ns = 1E-9s
        if time.time_ns() - (last_update + 1000000000) > 0:
            #set_motor_speed(0,0)
            pass

        #terminate the connection in case of very bad connection
        if time.time_ns() - (last_update + 30000000000) > 0:
            if DEBUG:
                print("Connection timeout!")
            break     
            
        ready = select.select([soc],[],[],0)
        if ready[0]:
            data, cur_ip_addr = soc.recvfrom(1024)
            if ip_addr == cur_ip_addr and data:
                #update the last received Counter
                last_update = time.time_ns()
                
                ID = data[0]

                if ID == dict.msg_dict["DV_STRAIGHT"]:
                    data2 = struct.unpack("!Bf",data)
                    cash = convert_to_motor(data2[1])
                    set_motor_speed(cash, cash)

                if ID == dict.msg_dict["DV_STOP"]:
                    set_motor_speed(0,0)


                if ID == dict.msg_dict["DV_ROTATE"]:
                    data2 = struct.unpack("!Bf",data)
                    cash = data2[1]
                    cash2 = cash * (-1)
                    set_motor_speed(convert_to_motor(cash2), convert_to_motor(cash))



                if ID == dict.msg_dict["DV_RAW_MODE"]:
                    data2 = struct.unpack("Bff",data)
                    set_motor_speed(data2[1], data2[2])
                    raw_mode = True

                #modes for cal
                if ID == dict.msg_dict["DV_CALL_STRAIGHT"]:
                    try:
                        data2 = struct.unpack("!Bff",data)
                        speed = convert_to_motor(data2[1])
                        duration = data2[2]
                        Drive.drive(speed, speed, duration)
                    except Exception as e:
                        print("ERROR 01 (",e,")")


                if ID == dict.msg_dict["DV_CALL_ROTATE"]:
                    try:
                        data2 = struct.unpack("!Bff",data)
                        speed = convert_to_motor(data2[1])
                        duration = data2[2]
                        Drive.drive(speed, -speed, duration)
                    except Exception as e:
                        print("ERROR 01 (",e,")")

            
            

if __name__ == "__main__":
    if os.fork() == 0:
        subprocess.run(["killall", "rtsp_server"])
        subprocess.run(["/home/pi/Carlos-s-Batmobile/rtsp-server/rtsp_server", "/home/pi/Carlos-s-Batmobile/rtsp-server/480p30fps2000000bit.conf"])
        print("Video Fail!")        
    else:
        while True:      
            try: 
                main()
                print ("Something went wrong, connection terminated and ready for new connection")
            except KeyboardInterrupt:
                #videostream.close()
                exit()




