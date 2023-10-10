import socket

# Producer details
local_address_and_port       = ("producer2", 50001)
local_ip                     = "producer2"
local_port                   = 50001
prod_id = "P02"

# Broker details
broker_address_and_port     = ("broker", 50010)
broker_ip                   = "broker"
broker_port                 = 50010

# Buffer Size
bufferSize          = 1024

# Create a datagram socket
local_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
local_socket.bind((local_ip, local_port))

print("Producer up and running.")


timer = 0;
frame_no = 1;

header_length = "05"

while(True):

    if(timer < 30000000):
        timer += 1

    else:
        timer = 0
        frame_no += 1
        print("Frame " + str(frame_no))
        msg = "From P2: frame " + str(frame_no)
        header_and_message = header_length + prod_id + msg
        local_socket.sendto(str.encode(header_and_message), broker_address_and_port)



