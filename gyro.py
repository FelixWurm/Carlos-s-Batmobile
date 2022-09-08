import smbus
import math
from time import sleep as sl

# known problems:
# no reconnect after Gyro Fail possible

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#Acceleration Configuration Register
ACCEL_CONFIG_REG = 0x1C

#Gyro configuration
GYRO_CONFIG_REG = 0x1B

read_fail = True


def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def init():
    bus = smbus.SMBus(1)
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0b00000000)
    
    #setup the Gyro modul
    bus.write_byte_data(address, GYRO_CONFIG_REG, 0)
    #Setup:
    bus.write_byte_data(address, ACCEL_CONFIG_REG, 0b00000000)

def read_acl(axis):
    try:
        if(axis == "x"):
            return  read_word_2c(0x43) / 131
        if(axis == "y"):
            return  (read_word_2c(0x45) / 131)
        if(axis == "z"):
            return  read_word_2c(0x47) / 131
    except:
        print ("Accelerometer Fail")
        read_fail = True
        return 0

def read_gyro(axis):
    try:
        if(axis == "x"):
            return read_word_2c(0x3b)/ (16384) 
        if(axis == "y"):
            return (read_word_2c(0x3d)/ (16384))
        if(axis == "z"):
            return read_word_2c(0x3f)/ (16384)
    except:
        print ("Gyro Fail")
        read_fail = True
        return 0    


bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect 

 
while(True):
    if read_fail == True:
        init()
        read_fail = False
    else:
        x = 0
        for y in range (0,100):
            x = x + read_gyro("y")
        
        format_float = "{:.4f}".format(x/100)
        print(format_float)
    
    
