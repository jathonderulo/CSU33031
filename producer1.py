import socket
from random import randint

# Producer details
local_address_and_port       = ("producer", 50000)
local_ip                     = "producer"
local_port                   = 50000
local_id = "P01"

# Broker details
broker_address_and_port     = ("broker", 50010)
broker_ip                   = "broker"
broker_port                 = 50010

# Buffer Size
bufferSize          = 50000

# Create a datagram socket
local_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
local_socket.bind((local_ip, local_port))

print("Producer up and running.")


timer = 0;
frame_no = 1;

packet_header_length = "15"
max_frames = "301"
stop = False
while(True):

    if(timer < 30000000):
        timer += 1

    else:
        timer = 0

        if randint(0, 15) == 5:
            if stop:
                print("Continue")

            else:
                print("Pause")
            stop = not stop

        # Read bytes from a file
        if not stop:
            with open('FrameSamples1/frame' + str(frame_no).zfill(3) + '.png', 'rb') as file:
                file_bytes = file.read()

            print("Frame " + str(frame_no))
            
            request_type = "P"
            msg = file_bytes
            text = "Frame number " + str(frame_no) + " from P01"
            length_of_text = str(len(text)).zfill(3)
            header = request_type + str(frame_no).zfill(3) + max_frames + length_of_text + local_id
            frame_no += 1
            header_and_message = str.encode(packet_header_length + header + text) + msg
            local_socket.sendto(header_and_message, broker_address_and_port)



