import socket
from random import randint
from time import sleep

# Subscriber details
sub_address_and_port        = ("subscriber2", 50021)
sub_ip                      = "subscriber2"
sub_port                    = 50021
local_id = "S02"

# Broker details
broker_address_and_port     = ("broker", 50010)
broker_ip                   = "broker"
broker_port                 = 50010

# Buffer Size
bufferSize          = 50000

# Create a datagram socket
sub_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Create a datagram socket
sub_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
sub_socket.bind((sub_ip, sub_port))
print("Subscriber up and running.")


def send_subscribe_request(prod_id, sub_id, broker_address_and_port):
    request_type = "S"
    header_length = "03"
    header = str.encode(header_length + request_type)
    message = str.encode(prod_id + sub_id)
    header_and_message = header + message
    # print(header_and_message.decode())
    sub_socket.sendto(header_and_message, broker_address_and_port)
    # print("Sent subscribe request")
    # ack_code = sub_socket.recvfrom(bufferSize)

    # TODO handle ack code here
def send_unsubscribe_request(prod_id, sub_id, broker_address_and_Port):
    request_type = "U"
    header_length = "03"
    header = str.encode(header_length + request_type)
    message = str.encode(prod_id + sub_id)
    header_and_message = header + message
    # print(header_and_message.decode())
    sub_socket.sendto(header_and_message, broker_address_and_port)
    # print("Sent unsubscribe request")
def toggle_subscribe(sub_id):
    toggle_sub(sub_id, local_id, broker_address_and_port, subscribed)
def toggle_sub(prod_id, sub_id, broker_address_and_port, subscribed):
    if subscribed:
        send_unsubscribe_request(prod_id, sub_id, broker_address_and_port)
        subscribed = False

    else:
        send_subscribe_request(prod_id, sub_id, broker_address_and_port)
        subscribed = True
def randomly_subscribe():
    if randint(0, 1) == 1:
        sub_id = "P01"
    else:
        sub_id = "P02"
        
    num = 500000
    while(True):
        if randint(0, 1000000) == num:
            toggle_subscribe(sub_id)
            break

subscribed = False
subbed_to = "P02"
toggle_subscribe(subbed_to)
subscribed = not subscribed

while(True):

    if subscribed:
        message, address = sub_socket.recvfrom(bufferSize)

        header_length = int(message[:2])
        header_decoded = message[:header_length].decode()
        # print("Header is : " + header_decoded)
        request_type = header_decoded[2]
        # print(request_type)
        if request_type == "P":
            text_length = int(header_decoded[-6:-3])
            # print("Received a packet from " + header_decoded[header_length-3:])
            # print("Frame " + header_decoded[3:5] + " of " + header_decoded[5:7])
            print("Text: " + message[header_length:(header_length+text_length)].decode())
            # Open a new file in binary write mode
            with open('sub2/output' + header_decoded[3:6] + '.png', 'wb') as new_file:
                # Write the bytes to the new file
                new_file.write(message[header_length + text_length:]) 

        if randint(0, 15) == 5:
            toggle_subscribe(subbed_to)
            subscribed = False
            # print("Unsubscribed!")
            message, address = sub_socket.recvfrom(bufferSize)
            header_length = int(message[:2])
            header_decoded = message[:header_length].decode()
            if header_decoded[2] == "A":
                print("Successfully unsubscribed from " + header_decoded[3:6])


    else:
        randomly_subscribe()
        # print("Subscribed!")
        subscribed = True
        message, address = sub_socket.recvfrom(bufferSize)
        header_length = int(message[:2])
        header_decoded = message[:header_length].decode()
        if header_decoded[2] == "A":
            print("Successfully subscribed to " + header_decoded[3:6])
