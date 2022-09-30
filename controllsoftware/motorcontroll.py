import RPi.GPIO as GPIO
import time

# Motor control Pin
left_fwd = 12
left_bwd = 26
right_fwd = 13
right_bwd = 19

# Drive...
class Drive:
    def __init__(self):
        self.end_time = 0

        #if 0 no movement, if 1 forwards, -1 = backwards
        self.drive_direction = 0

        # Set up the GPIO stuff
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(left_fwd, GPIO.OUT)
        GPIO.setup(right_fwd, GPIO.OUT)
        GPIO.setup(left_bwd, GPIO.OUT)
        GPIO.setup(right_bwd, GPIO.OUT)

        # Setup some PWM stuff
        self.pi_pwm_l = GPIO.PWM(left_fwd, 1000)
        self.pi_pwm_l.start(0)

        self.pi_pwm_r = GPIO.PWM(right_fwd, 1000)
        self.pi_pwm_r.start(0)

        self.pi_pwm_l_bwd = GPIO.PWM(left_bwd, 1000)
        self.pi_pwm_l_bwd.start(0)

        self.pi_pwm_r_bwd = GPIO.PWM(right_bwd, 1000)
        self.pi_pwm_r_bwd.start(0)


        self.speed_r = 0
        self.speed_l = 0


    def drive(self, speed_l, speed_r, dv_time):
        # check for correct input
        if (0 < speed_l < 40) or (-40 < speed_l < 0):
            print("incorrect Input speed_l, must be between -100 to -40 or 40 to 100")
            return

        if (0 < speed_r < 40) or (-40 < speed_r < 0):
            print("incorrect Input speed_r, must be between -100 to -40 or 40 to 100")
            return

        self. set_motor_speed(speed_l, speed_r)
        self.end_time = time.time_ns() + (dv_time * 1000000000)

    def run(self):
        if self.end_time < time.time_ns() and self.end_time != 0:
            self.set_motor_speed(0, 0)
            self.end_time = 0


    def set_motor_speed(self, speed_l: int, speed_r: int):
        self.speed_l = self.value_check(speed_l)
        self.speed_r = self.value_check(speed_r)

        if self.speed_l == self.speed_r:
            if self.speed_l == 0:
                self. drive_direction = 0
            elif self.speed_r > 0:
                self.drive_direction = 1
            else:
                self.drive_direction = -1
        else:
            self.drive_direction = 0
        
        if self.speed_l == 0:
            self. pi_pwm_l.ChangeDutyCycle(0)
            self.pi_pwm_l_bwd.ChangeDutyCycle(0)
        else:
            if self.speed_l > 0:
                self.pi_pwm_l.ChangeDutyCycle(speed_l)
                self.pi_pwm_l_bwd.ChangeDutyCycle(0)
            else:
                self.pi_pwm_l.ChangeDutyCycle(0)
                self.pi_pwm_l_bwd.ChangeDutyCycle(speed_l * (-1))

        if self.speed_r == 0:
            self.pi_pwm_r.ChangeDutyCycle(0)
            self.pi_pwm_r_bwd.ChangeDutyCycle(0)
        else:
            if self.speed_r > 0:
                self.pi_pwm_r.ChangeDutyCycle(speed_r)
                self.pi_pwm_r_bwd.ChangeDutyCycle(0)
            else:
                self.pi_pwm_r.ChangeDutyCycle(0)
                self.pi_pwm_r_bwd.ChangeDutyCycle(speed_r * (-1))

    def value_check(value):
        if value > 100:
            print("value was to big! (", value, ")")
            value = 100
        elif value < -100:
            print("Value was to small! (", value, ")")

        return value

    def get_direction(self):
        return self.drive_direction

    def get_speed(self):
        return (self.speed_l, self.speed_r)