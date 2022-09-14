msg_dict = {
    "STAY_ALLIVE"   : int(0),       #no additional value
    "DV_STRAIGHT"   : int(1),       #Float(speed -100 - 100)
    "DV_ROTATE"     : int(2),       #Float(speeed -1ßß - 100)
    "DV_RAW_MODE"   : int(3),       #Float(motor L), Float(motor R)
    "CONN_REQUEST"  : int(4),       #Request a conecction, No additional value
    "CONN_ACCEPT"   : int(5),       #Accept a connection, NO additional value
    "DV_STOP"       : int(6),       #no additional value
    "ACK"           : int(7),       #singal that something was recived
    "READY_CONN"    : int(9),        #ready for connection(UDP auto discovery)
    "ERROR_CONN"    : int(10)       #send this signal ig there is in invalid Connection attempt

}

#in order to connect to the server send a CONN_REQUEST and wait for a CONN_ACCEPT.