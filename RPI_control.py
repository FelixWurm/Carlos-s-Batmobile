import select, sys, struct
import RPi.GPIO as GPIO
from time import sleep as sl
import socket
import asyncio
import websockets

#Debug
DEBUG = True


#Motorconroll Pin
left_fwd = 12
left_bwd = 26
right_fwd = 13
right_bwd = 19



#auto Discovery
msg_udp_dict = {
    "REDY_CON" : int(64),
    "ERROR" : int(128)
}

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



    if(speed_l > 0):
        pi_pwm_l.ChangeDutyCycle(speed_l)
    else:
        pi_pwm_l_bwd.ChangeDutyCycle(speed_l*(-1))


    if(speed_r > 0):
        pi_pwm_r.ChangeDutyCycle(speed_r)
    else:
        pi_pwm_r_bwd.ChangeDutyCycle(speed_r*(-1))



    #wait for the specified Time
    sl(time)
    print("running")

    pi_pwm_l.ChangeDutyCycle(0)
    pi_pwm_r.ChangeDutyCycle(0)
    pi_pwm_l_bwd.ChangeDutyCycle(0)
    pi_pwm_r_bwd.ChangeDutyCycle(0)




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
    drive_(speed, time);


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







#TCP
def tcp_setup():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind Server to localhost
    soc.bind(("", 50000))

    #Listen vor incomming connections
    soc.listen(1)# wait for client connection
    return soc



async def http_interface(http_port):
    
    async with websockets.connect("ws:localhost:"+ string(http_port)) as websocket:
        await websocket.send("WIR SIND DIE ROBOTER")
        await websocket.reciv()

asyncio.run(http_interface(50001))


def main():
    soc = tcp_setup()
    #send discovery signal once, should by send every minuit, nonblocking server requiert. 
    udp_soc = udp_discovery_setup()
    udp_discovery(udp_port, udp_addr, udp_soc,msg_udp_dict["REDY_CON"])
    
    
    print("IP:", get_local_ip())

    while(True):
        
        
        conn, addr = soc.accept()
        
        
        
        
        print("Connectet to ", addr)
    
        while(True):
            try:
                data = conn.recv(1024)
                print(data)
                ID = data[0]
                
                if ID == int(1):
                    data = struct.unpack("!Bff",data)
                    drive_dst(data[1], data[2])
                if ID == int(0):
                    conn.sendall(0xFF)

            except Exception as e:
                print(e)
                break
            finally:
                conn.disconnect()
            
    
main()




