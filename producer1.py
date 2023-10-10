import socket

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

packet_header_length = "06"
while(True):

    if(timer < 30000000):
        timer += 1

    else:
        timer = 0

        # Read bytes from a file
        with open('First20Frames/frame' + str(frame_no).zfill(3) + '.png', 'rb') as file:
            file_bytes = file.read()

        print("Frame " + str(frame_no))
        frame_no += 1

        msg = file_bytes
        request_type = "P"
        header = request_type + local_id
        header_and_message = str.encode(packet_header_length + header) + msg
        local_socket.sendto(header_and_message, broker_address_and_port)



