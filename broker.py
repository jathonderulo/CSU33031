import socket
from time import sleep

class Producer:
    def __init__(self, prod_id):
        self.prod_id = prod_id
        self.subs_list = []

class Subscriber:
    def __init__(self, sub_id, sub_address_and_port):
        self.sub_id = sub_id
        self.sub_address_and_port = sub_address_and_port
        self.subscribed_to_list = []

# Broker details
broker_address_and_port     = ("0.0.0.0", 50010)
broker_ip                   = "0.0.0.0"
broker_port                 = 50010

# Subscriber details
sub1_address_and_port        = ("subscriber", 50020)
sub1_ip                      = "subscriber"
sub1_port                    = 50020

sub2_address_and_port        = ("subscriber2", 50021)
sub2_ip                      = "subscriber2"
sub2_port                    = 50021

prod1 = Producer("P01")
prod2 = Producer("P02")
producers_list: [Producer] = [prod1, prod2]

# sub1 = Subscriber("S01")
# sub2 = Subscriber("S02")
subscribers_list: [Subscriber] = []

# Buffer Size
bufferSize                  = 50000

# Create datagram sockets
broker_socket      = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
broker_socket.bind((broker_ip, broker_port))

print("Broker up and running.")

def subscribe(prod_id, sub_id, sub_address_and_port):
    """ 
    Lets a consumer subscribe to a producer 

    returns a code that will be interpreted by function caller
    """
    # TODO implement subscribe + error checking for sub_id / prod_id
    
    # Check that subscriber is in our list, if not, add it 
    sub_found = False
    for sub in subscribers_list:
        if sub.sub_id == sub_id:
            sub_found = True
            break
    
    if sub_found == False:
        sub = Subscriber(sub_id, sub_address_and_port)
        subscribers_list.append(sub) 

    # Check that producer id is correct
    prod_found = False
    for prod in producers_list:
        if prod.prod_id == prod_id:
            prod_found = True
            prod.subs_list.append(sub)
            sub.subscribed_to_list.append(prod)
            break
    
    if prod_found == False:
        print("Subscribe failed, no producer found.")
        return -1

    print(sub_id + " has successfully subscribed to " + prod_id)

    # Send ack
    msg = "09A" + prod_id + sub_id
    sleep(0.5)
    broker_socket.sendto(str.encode(msg), sub_address_and_port)


def unsubscribe(prod_id, sub_id, sub_address_and_port):
    # TODO implement unsubscribe + error checking for sub_id / prod_id
    # TODO I have to check sub_id exists, prod_id exists, and that sub is subscribed to prod, and prod has sub as a subscriber

    # Check sub exists in our list
    sub_found = False
    for sub in subscribers_list:
        # print(sub.sub_id + " " + sub_id)
        if sub.sub_id == sub_id:
            sub_found = True
            break

    if not sub_found:
        print("sub not found!")
        return -1 # Error code ? 
    
    # Check prod exists in our list
    prod_found = False
    for prod in producers_list:
        if prod.prod_id == prod_id:
            prod_found = True
            break

    if not prod_found:
        print("prod not found!")
        return -2 # Error code ?
    
    # Check subscribed
    subscribed = False
    if prod in sub.subscribed_to_list:
        prod.subs_list.remove(sub)
        sub.subscribed_to_list.remove(prod)

    print(sub_id + " has successfully unsubscribed from " + prod_id)
    # Send ack
    sleep(0.5)
    msg = "09A" + prod_id + sub_id
    broker_socket.sendto(str.encode(msg), sub_address_and_port)


while(True):
    # breaking up the header and payload
    message, address = broker_socket.recvfrom(bufferSize)
    header_length = int(message[:2])
    header = message[:header_length]

    # print(header_length)

    packet_request_type = message[:6].decode()[2]
    # print("Request type is: " + packet_request_type)
    
    if packet_request_type == "S": #example message = 03SP01S01
        message_as_string = message.decode()
        # print(message_as_string)
        prod_id = message_as_string[header_length:][:3]
        # print(prod_id)
        sub_id = message_as_string[header_length:][3:6]
        subscribe(prod_id, sub_id, address)

    elif packet_request_type == "P": # packet
        prod_id_last_digit = int(message[:header_length].decode()[header_length-1]) 
        # print(int(prod_id_last_digit))
        print("Received packet from " + header[-3:].decode())
        if len(producers_list[prod_id_last_digit-1].subs_list) != 0:
            for subscriber in producers_list[prod_id_last_digit-1].subs_list:
                # print("Broker sent msg! ")
                broker_socket.sendto(message, subscriber.sub_address_and_port)
        else:
            print("Received packet from P0" + str(prod_id_last_digit) + " but P0" + str(prod_id_last_digit) + " has no subscribers")

    elif packet_request_type == "U":
        message_as_string = message.decode()
        # print(message_as_string)
        prod_id = message_as_string[header_length:][:3]
        sub_id = message_as_string[header_length:][3:6]
        unsubscribe(prod_id, sub_id, address)





