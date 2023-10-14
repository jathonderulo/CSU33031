import socket
from random import randint

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

local_subscribed_to_list = []

def send_subscribe_request(prod_id, sub_id, broker_address_and_port):
    request_type = "S"
    header_length = "03"
    header = str.encode(header_length + request_type)
    message = str.encode(prod_id + sub_id)
    header_and_message = header + message
    print(header_and_message.decode())
    sub_socket.sendto(header_and_message, broker_address_and_port)
    print("Sent subscribe request")
    # ack_code = sub_socket.recvfrom(bufferSize)

    # TODO handle ack code here
def send_unsubscribe_request(prod_id, sub_id, broker_address_and_Port):
    request_type = "U"
    header_length = "03"
    header = str.encode(header_length + request_type)
    message = str.encode(prod_id + sub_id)
    header_and_message = header + message
    print(header_and_message.decode())
    sub_socket.sendto(header_and_message, broker_address_and_port)
    print("Sent unsubscribe request")
def toggle_subscribe():
    toggle_sub("P02", local_id, broker_address_and_port, subscribed)
def toggle_sub(prod_id, sub_id, broker_address_and_port, subscribed):
    if subscribed:
        send_unsubscribe_request(prod_id, sub_id, broker_address_and_port)
        subscribed = False

    else:
        send_subscribe_request(prod_id, sub_id, broker_address_and_port)
        subscribed = True
def randomly_subscribe():
    num = 5000000
    while(True):
        if randint(0, 10000000) == num:
            toggle_subscribe()
            break

subscribed = False
toggle_subscribe()
subscribed = not subscribed

while(True):
    if subscribed:
        message, address = sub_socket.recvfrom(bufferSize)

        header_length = int(message[:2])
        header_decoded = message[:header_length].decode()
        # print("Header is : " + header_decoded)
        if header_decoded[2] == "P":
            print("Received a packet from " + header_decoded[header_length-3:])
            print("Frame " + header_decoded[3:5] + " of " + header_decoded[5:7])
            # Open a new file in binary write mode
            with open('sub2/output' + header_decoded[3:5] + '.png', 'wb') as new_file:
                # Write the bytes to the new file
                new_file.write(message[header_length:])
        
        if randint(0, 10) == 5:
            toggle_subscribe()
            subscribed = False
            print("Unsubscribed")

    else:
        randomly_subscribe()
        print("Subscribed!")
        subscribed = True
