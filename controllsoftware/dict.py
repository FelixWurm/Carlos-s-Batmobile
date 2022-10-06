msg_dict = {
    "STAY_ALIVE"        : int(0),        #no additional value 
    "DV_STRAIGHT"       : int(1),       #Float(speed -100 - 100)
    "DV_ROTATE"         : int(2),       #Float(speed -1ßß - 100)
    "DV_RAW_MODE"       : int(3),       #Float(motor L), Float(motor R)
    "CONN_REQUEST"      : int(4),       #Request a connection, No additional value
    "CONN_ACCEPT"       : int(5),       #Accept a connection, NO additional value
    "DV_STOP"           : int(6),       #no additional value
    "ACK"               : int(7),       #signal that something was receive
    "POS_CURR_LEFT"     : int(8),       #distance driven by left front wheel <- laser
    "READY_CONN"        : int(9),       #ready for connection(UDP auto discovery)
    "ERROR_CONN"        : int(10),      #send this signal ig there is in invalid Connection attempt
    "NO_MODE"           : int(11),      #only for internal 
    "DV_CALL_STRAIGHT"  : int(12),      #only for testing, first float speed , second time
    "DV_CALL_ROTATE"    : int(13),      #only for testing, first float speed , second time
    "POS_CURRENT_RAW"   : int(14),      #long x, long y
    "POS_RESET"         : int(15),      #reset the Position to 0
    "DATA_PACKET"       : int(16),      #all data, float[GYRO_X, GYRO_Y, GYRO_Z, ACCEL_X,ACCEL_Y,ACCEL_Z,MOUSE_X, MOUSE_Y,LASER,speed_l, speed_r]
    "DATA_PACKET_ENABLE": int(17),      #enable Transfere of as many data as possible
    "DATA_PACKET_DISABLE":int(18)       #disable this transmission of data
}



#in order to connect to the server send a CONN_REQUEST and wait for a CONN_ACCEPT.
