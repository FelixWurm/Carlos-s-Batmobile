# Script that runs on the RPi in order to control the movement and the Sensor data
import os
import select
import socket
import struct
import subprocess
import sys
import time
from dataclasses import dataclass
import gyro_lib

import RPi.GPIO as GPIO
import dict
import evdev

try:
    import VL53L0X
except:
    print("Laser lib not found!")


import positioner

# Debug
DEBUG = True


# Objects to store the position values
@dataclass
class Point:
    x: float = 0
    y: float = 0


@dataclass
class Move:
    start_position: Point
    end_position: Point
    direction: int

    move_mode: int = dict.msg_dict["NO_MODE"]
    move_speed: int = 0
    move_start: int = 0
    move_end: int = 0


# Motor control Pin
left_fwd = 12
left_bwd = 26
right_fwd = 13
right_bwd = 19

udp_port = 25565
udp_addr = "169.254.2.1"

# Set up the GPIO stuff
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_fwd, GPIO.OUT)
GPIO.setup(right_fwd, GPIO.OUT)
GPIO.setup(left_bwd, GPIO.OUT)
GPIO.setup(right_bwd, GPIO.OUT)

# Setup some PWM stuff
pi_pwm_l = GPIO.PWM(left_fwd, 1000)
pi_pwm_l.start(0)

pi_pwm_r = GPIO.PWM(right_fwd, 1000)
pi_pwm_r.start(0)

pi_pwm_l_bwd = GPIO.PWM(left_bwd, 1000)
pi_pwm_l_bwd.start(0)

pi_pwm_r_bwd = GPIO.PWM(right_bwd, 1000)
pi_pwm_r_bwd.start(0)



#if 0 no movement, if 1 forwards, -1 = backwards
drive_direction = 0



# Drive...
class Drive:
    def __init__(self):
        self.end_time = 0

    def drive(self, speed_l, speed_r, dv_time):
        # check for correct input
        if (0 < speed_l < 40) or (-40 < speed_l < 0):
            print("incorrect Input speed_l, must be between -100 to -40 or 40 to 100")
            return

        if (0 < speed_r < 40) or (-40 < speed_r < 0):
            print("incorrect Input speed_r, must be between -100 to -40 or 40 to 100")
            return

        set_motor_speed(speed_l, speed_r)
        self.end_time = time.time_ns() + (dv_time * 1000000000)

    def run(self):
        if self.end_time < time.time_ns() and self.end_time != 0:
            set_motor_speed(0, 0)
            self.end_time = 0


def set_motor_speed(speed_l: int, speed_r: int):
    global drive_direction
    speed_l = value_check(speed_l)
    speed_r = value_check(speed_r)

    if speed_l == speed_r:
        if speed_l == 0:
            drive_direction = 0
        elif speed_r > 0:
            drive_direction = 1
        else:
            drive_direction = -1
    else:
       drive_direction = 0
    
    if speed_l == 0:
        pi_pwm_l.ChangeDutyCycle(0)
        pi_pwm_l_bwd.ChangeDutyCycle(0)
    else:
        if speed_l > 0:
            pi_pwm_l.ChangeDutyCycle(speed_l)
            pi_pwm_l_bwd.ChangeDutyCycle(0)
        else:
            pi_pwm_l.ChangeDutyCycle(0)
            pi_pwm_l_bwd.ChangeDutyCycle(speed_l * (-1))

    if speed_r == 0:
        pi_pwm_r.ChangeDutyCycle(0)
        pi_pwm_r_bwd.ChangeDutyCycle(0)
    else:
        if speed_r > 0:
            pi_pwm_r.ChangeDutyCycle(speed_r)
            pi_pwm_r_bwd.ChangeDutyCycle(0)
        else:
            pi_pwm_r.ChangeDutyCycle(0)
            pi_pwm_r_bwd.ChangeDutyCycle(speed_r * (-1))


def value_check(value):
    if value > 100:
        print("value was to big! (", value, ")")
        value = 100
    elif value < -100:
        print("Value was to small! (", value, ")")

    return value


def drive_(speed, duration):
    drive(speed, speed, duration)


# speed in M at a given speed, from 100 to 40 in increments of 10
speed_distance = [0.23, 0.1975, 0.18, 0.16, 0.1375, 0.12, 0.09]






# Function to get your local ip address
def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
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


def udp_discovery(discovery_port, discovery_address, udp_soc, msg):
    udp_soc.sendto(struct.pack("!B", msg), (discovery_address, discovery_port))


class MvObserver:
    def __init__(self) -> None:
        # mode (straight, rotate since the last change)
        self.last_mode = dict.msg_dict["NO_MODE"]
        self.last_speed = 0
        self.last_mode_beginning = 0
        self.last_start_position = Point(0, 0)
        self.last_direction = 0

        self.list_of_moves = []
        self.position = positioner

    def move(self, mode, speed):

        # lok if the mode has changed significantly, if so save the old move, and calculate start and end position.
        if not (mode == self.last_mode and speed == self.last_speed):
            # Filter out just start moving
            if self.last_mode == dict.msg_dict["NO_MODE"]:
                # comes from no move to some movement
                self.last_mode = mode
                self.last_speed = speed
                self.last_mode_beginning = time.time_ns()


            else:
                # there was some change, so there needs to by an event appended

                # save the current data
                cache_move = Move
                cache_move.move_speed = self.last_speed
                cache_move.move_type = self.last_mode
                cache_move.move_start = self.last_mode_beginning
                cache_move.start_position = self.last_start_position

                cache_move.move_end = time.time_ns()

                self.list_of_moves.append(cache_move)

                # save the new last set data
                self.last_mode = mode
                self.last_speed = speed
                self.last_mode_beginning = time.time_ns()

    def cal_end_position(self):
        if self.move_mode == dict.msg_dict["NO_MODE"]:
            return

        if self.move_mode == dict.msg_dict["DV_STRAIGHT"]:
            #calculate the position based on passed Time
            #self.position.add_position()
            pass

        if self.move_mode == dict.msg_dict["DV_ROTATE"]:
            #calculate the position based on passed Time
            #self.position.add_rotation()
            pass
    

    def get_forward(self):
        if self.last_mode ==dict.msg_dict["DV_ROTATE"]:
            return None

        elif self.move_mode == dict.msg_dict["DV_STRAIGHT"]:
            if self.last_speed > 0:
                return True
            else:
                return False
    def get_position(self):
        return self.position.get_position()
    
    def get_angle(self):
        return self.position.get_rotation()



# UDP
def udp_setup():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind Server to localhost
    soc.bind(("", 50000))

    return soc


def udp_connect(soc: socket):
    counter = 0
    while True:
        data, addr = soc.recvfrom(1024)
        if data[0] == dict.msg_dict["CONN_REQUEST"]:
            soc.sendto(struct.pack("!B", dict.msg_dict["CONN_ACCEPT"]), addr)
            soc.setblocking(0)
            return addr
        else:
            counter = counter + 1
            print("connection attempt with invalid init sequence, open for retries : ", counter)
            soc.sendto(struct.pack("!B", dict.msg_dict["ERROR_CONN"]), addr)


# converts a number from -100 to 100 toto -100-40, 40-100
def convert_to_motor(speed_input):
    speed_input = speed_input * 0.6
    if speed_input < 0:
        speed_input = speed_input - 40
    else:
        speed_input = speed_input + 40

    return speed_input


def calculate_position(mode, duration, speed, last_position):
    if mode == "R":
        pass
    if mode == "D":
        pass


def find_mouse():
    device = None
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for d in devices:
        if 'Mouse' in d.name:
            device = d
            print('Found %s at %s...' % (d.name, d.fn))
    return device

observer = MvObserver()

def compile_data(gyro , mouse_x, mouse_y ,wheel_rotation ):
    if gyro is not None:
        gx = gyro.read_gyro("x")
        gy = gyro.read_gyro("y")
        gz = gyro.read_gyro("z")

        ax = gyro.read_acl("x")
        ay = gyro.read_acl("y")
        az = gyro.read_acl("z")

        rot_x = gyro.get_x_rotation(gx,gy,gz)
        rot_y = gyro.get_y_rotation(gx,gy,gz)

    else:
        gx = 0
        gy = 0
        gz = 0

        ax = 0
        ay = 0
        az = 0

        rot_x = 0
        rot_y = 0

    return struct.pack("!Bdfffffffffff",dict.msg_dict["DATA_PACKET"],time.time(),gx,gy,gz,ax,ay,az,rot_x,rot_y, mouse_x,mouse_y,wheel_rotation)

def main():
    global observer
    global drive_direction
    # set up the TCP server
    soc = udp_setup()

    print("IP:", get_local_ip())

    # send discovery signal once, should be sent every minuit, nonblocking server required.
    udp_soc = udp_discovery_setup()
    udp_discovery(udp_port, udp_addr, udp_soc, dict.msg_dict["READY_CONN"])

    # try to connect to a UDP Host:
    ip_addr = udp_connect(soc)

    print("Connected to:", ip_addr)

    last_update = time.time_ns()

    # Idee: Nach jeder veränderung der Geschwindigkeit Die Position neu bestimmen

    # init drive class
    drive = Drive()

    #read laser data
    way = 0
    mean = 0
    allDist = 0
    height = False
    count_loop = 0

    # Create a VL53L0X object
    try:
        laser = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
        # I2C Address can change before laser.open()
        # laser.change_address(0x32)
        laser.open()
        # Start ranging
        laser.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
    except:
        laser = None


    #Create a Gyro object
    try:
        gyro = gyro_lib.gyro()
        print("Gyro Connected!")
    except Exception as e:
        gyro = None
        print("No Gyro Connected! (", e, ")")


    # position (Mouse sending)
    pos_x = 0
    pos_y = 0

    mouse = find_mouse()
    #assert mouse is not None

    while True:
        drive.run()

        # stop the motor in case of bad connection
        # 1ns = 1E-9s
        if time.time_ns() - (last_update + 1000000000) > 0:
            # set_motor_speed(0,0)
            pass

        # terminate the connection in case of very bad connection
        if time.time_ns() - (last_update + 30000000000) > 0:
            if DEBUG:
                print("Connection timeout!")
            break

        #laser
        if laser is not None:
            count_loop = count_loop+1
            distance = laser.get_distance()
            allDist += distance
            if distance > 0:
                mean = allDist/count_loop #<- count for each loop
                if distance < (mean-10):
                    if(height == False):
                        height = True
                        #way += 31.73
                        if drive_direction == 1:
                            way += 1
                        elif drive_direction == -1:
                            way += -1
                if distance > mean: # might want the 10%, but mean is smaller due to dip in wheel
                    height = False
            #time.sleep(timing/1000000.00)

        sockets = [soc]
        if mouse is not None:#
            sockets.append(mouse)

        # read in mouse data
        read_ready, _, _ = select.select(sockets, [], [])

        for read_fds in read_ready:
            if read_fds == mouse:
                for event in mouse.read():
                    if event.type == evdev.ecodes.EV_REL:
                        if event.code == evdev.ecodes.REL_X:
                            #pos_x += event.value / (-284.195)
                            cache = event.value
                            if cache < 0:
                                pos_x += cache 
                            else:
                                pos_x += cache 
                        
                        if event.code == evdev.ecodes.REL_Y:
                            cache = event.value
                            if cache < 0:
                                pos_y += cache 
                            else:
                                pos_y += cache 
            if read_fds == soc:
                # send as a reply the current position:
                #msg = struct.pack("!Bdd", dict.msg_dict["POS_CURRENT_RAW"], pos_x, pos_y)
                #soc.sendto(msg, ip_addr)
                # send laser data:
                #if laser is not None:
                #    msg = struct.pack("!Bff", dict.msg_dict["POS_CURR_LEFT"], way, (way/10)) # do we want his here for simplicity or do we do it in Controllsoftware.py?
                #    soc.sendto(msg, ip_addr)

                #send all Data
                soc.sendto(compile_data(gyro,pos_x,pos_y,way ),ip_addr)


                data, cur_ip_addr = soc.recvfrom(1024)
                if ip_addr == cur_ip_addr and data:
                    # update the last received Counter
                    last_update = time.time_ns()

                    code = data[0]

                    if code == dict.msg_dict["DV_STRAIGHT"]:
                        data2 = struct.unpack("!Bf", data)
                        cache = convert_to_motor(data2[1])
                        set_motor_speed(cache, cache)

                    if code == dict.msg_dict["DV_STOP"]:
                        set_motor_speed(0, 0)

                    if code == dict.msg_dict["DV_ROTATE"]:
                        data2 = struct.unpack("!Bf", data)
                        cache = data2[1]
                        cache2 = cache * (-1)
                        set_motor_speed(convert_to_motor(cache2), convert_to_motor(cache))

                    if code == dict.msg_dict["DV_RAW_MODE"]:
                        data2 = struct.unpack("Bff", data)
                        set_motor_speed(data2[1], data2[2])
                        raw_mode = True

                    # modes for cal
                    if code == dict.msg_dict["DV_CALL_STRAIGHT"]:
                        try:
                            data2 = struct.unpack("!Bff", data)
                            speed = convert_to_motor(data2[1])
                            duration = data2[2]
                            drive.drive(speed, speed, duration)
                        except Exception as e:
                            print("ERROR 01 (", e, ")")

                    if code == dict.msg_dict["DV_CALL_ROTATE"]:
                        try:
                            data2 = struct.unpack("!Bff", data)
                            speed = convert_to_motor(data2[1])
                            duration = data2[2]
                            drive.drive(speed, -speed, duration)
                        except Exception as e:
                            print("ERROR 01 (", e, ")")
                    if code == dict.msg_dict["POS_RESET"]:
                        pos_x = 0
                        pos_y = 0
                        way = 0


if __name__ == "__main__":
    while True:
        try:
            main()
            print("Something went wrong, connection terminated and ready for new connection")
        except KeyboardInterrupt:
            # videostream.close()
            exit()
