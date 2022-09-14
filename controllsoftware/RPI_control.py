# Scribt that runs on the RPi in order to controll the Movment and the Sensor data


import select, sys, struct
import RPi.GPIO as GPIO
from time import sleep as sl
import time
import socket
import dict

#Debug
DEBUG = True


#Motorconroll Pin
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
def drive (speed_l, speed_r, time):
    #check for correct input
    if((0 < speed_l < 40)or (-40 < speed_l < 0)):
        raise Exception("incorrect Input speed_l, must be between -100 to -40 or 40 to 100" )

    if((0 < speed_r < 40)or (-40 < speed_r < 0)):
        raise Exception("incorrect Input speed_r, must be between -100 to -40 or 40 to 100" )

    set_motor_speed(speed_l, speed_r)


    #wait for the specified Time
    sl(time)
    print("running")

    pi_pwm_l.ChangeDutyCycle(0)
    pi_pwm_r.ChangeDutyCycle(0)
    pi_pwm_l_bwd.ChangeDutyCycle(0)
    pi_pwm_r_bwd.ChangeDutyCycle(0)

def set_motor_speed(speed_l : int, speed_r :int):
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
            return addr
        else:
            counter +1
            print("conection with invalid init sequenz, open for retrys")


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
    
    #try to connect to a UDP Server:
    ip_addr = udp_connect(soc)    
    
    
    #some RAW_Mode suff
    raw_mode = False
    last_update = time.clock_gettime_ns(0)
    
    #Odometrie
    list_of_moves = []
    start_position = [0,0]    
    current_position = [0,0]
    current_direction = [0,0] 

    #Idee: Nach jeder veränderung der Geschwindigkeit Die Position neu bestimmen


    while(True):     
        #stop the motor in case of bad connection      
        #1ns = 1E-9s
        if time.clock_gettime_ns(0) - (last_update + 1000000) < 0:
            set_motor_speed(0,0)

        #terminate the connection in case of very bad connection
        if time.clock_gettime_ns(0) - (last_update + 30000000) < 0:
              break     
            
    
        data, cur_ip_addr = soc.recvfrom(1024)
        if ip_addr == cur_ip_addr and data:
            #update the recived Counter
            last_update= time.clock_gettime_ns(0)
            
            ID = data[0]
            if ID == dict.msg_dict["DV_STRAIGHT"]:
                data = struct.unpack("!Bf",data)
                cash = convert_to_motor(data[1])
                set_motor_speed(cash, cash)

            if ID == dict.msg_dict["DV_STOP"]:
                set_motor_speed(0,0)


            if ID == dict.msg_dict["DV_ROTATE"]:
                data = struct.unpack("!Bf",data)
                cash = data[1]
                cash = cash *(-1)
                set_motor_speed(convert_to_motor(cash), convert_to_motor(data[1]))



            if ID == dict.msg_dict["DV_RAW_MODE"]:
                data = struct.unpack("Bff",data)
                set_motor_speed(data[1], data[2])
                raw_mode = True
                last_update = time.clock_gettime_ns(0)

            
            

if __name__ == "__main__":
    while True:         
        main()
        print ("Something went wrong, connection terminatet and ready for new connection")




