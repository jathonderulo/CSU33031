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
bufferSize          = 1024

# Create a datagram socket
local_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
local_socket.bind((local_ip, local_port))

print("Producer up and running.")


timer = 0;
frame_no = 1;

def image_to_bytes(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    return image_bytes


normallol_header_length = "05"
packet_header_length = "06"
while(True):

    if(timer < 30000000):
        timer += 1

    else:
        timer = 0
        frame_no += 1
        print("Frame " + str(frame_no))
        msg = "HELLO SUBBED DO YOU SEE THIS " + str(frame_no)

        request_type = "P"
        header = request_type + local_id
        header_and_message = packet_header_length + header + msg
        # print(header_and_message)
        local_socket.sendto(str.encode(header_and_message), broker_address_and_port)



