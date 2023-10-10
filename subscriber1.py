import socket
import random

# Subscriber details
sub_address_and_port        = ("subscriber", 50020)
sub_ip                      = "subscriber"
sub_port                    = 50020
local_id = "S01"

# Broker details
broker_address_and_port     = ("broker", 50010)
broker_ip                   = "broker"
broker_port                 = 50010

# Buffer Size
bufferSize          = 1024

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

def toggle_sub(prod_id, sub_id, broker_address_and_port, subscribed):
    if subscribed:
        send_unsubscribe_request(prod_id, sub_id, broker_address_and_port)
        subscribed = False

    else:
        send_subscribe_request(prod_id, sub_id, broker_address_and_port)
        subscribed = True

toggle_after = 4

packets_recv_num = 0

subscribed = False
toggle_sub("P01", local_id, broker_address_and_port, subscribed)
subscribed = not subscribed

while(True):
    message, address = sub_socket.recvfrom(bufferSize)
    packets_recv_num += 1
    if packets_recv_num == toggle_after:
        toggle_sub("P01", local_id, broker_address_and_port, subscribed)
        subscribed = not subscribed
        toggle_after += 4
    print(message.decode())
    header_length = message[:2]
    message_as_string = message.decode()
    if message[2] == "P":
        print("Received packet from" + message[3:header_length] + ", message is: " + message[header_length:] )