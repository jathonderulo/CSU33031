import socket
from random import randint

# Producer details
local_address_and_port       = ("producer2", 50001)
local_ip                     = "producer2"
local_port                   = 50001
local_id = "P02"

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

packet_header_length = "10"
max_frames = "20"
stop = False
while(True):

    if(timer < 30000000):
        timer += 1

    else:
        timer = 0

        if randint(0, 15) == 5:
            print("Producing frames = " + str(stop))
            stop = not stop

        if not stop:
            # Read bytes from a file
            with open('First20Frames/frame' + str(frame_no).zfill(3) + '.png', 'rb') as file:
                file_bytes = file.read()

            print("Frame " + str(frame_no))

            msg = file_bytes
            request_type = "P"
            header = request_type + str(frame_no).zfill(2) + max_frames + local_id
            frame_no += 1
            header_and_message = str.encode(packet_header_length + header) + msg
            local_socket.sendto(header_and_message, broker_address_and_port)



