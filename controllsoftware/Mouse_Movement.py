import evdev

#for listing all devices

#for dev in [evdev.InputDevice(fn) for fn in evdev.list_devices()]:
#    print(str(dev))

if __name__ == '__main__':
    X = 0
    Y = 0
    X_MAX = 200
    Y_MAX = 200
    DEVICE = None

    DEVICES = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    for d in DEVICES:
        if 'Mouse' in d.name:
            DEVICE = d
            print('Found %s at %s...' % (d.name, d.fn))
            break

    if DEVICE:
        print('Started listening to device')
        for event in DEVICE.read_loop():
            if event.type == evdev.ecodes.EV_REL:
                if event.code == evdev.ecodes.REL_X:
                    X += event.value
                if event.code == evdev.ecodes.REL_Y:
                    Y += event.value

                if X > X_MAX:
                    X = X_MAX
                if X < 0:
                    X = 0

                if Y > Y_MAX:
                    Y = Y_MAX
                if Y < 0:
                    Y = 0

                #print('X=%d Y=%d' % (X, Y))
                if
