import socket

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
bufferSize                  = 1024

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
        print("SUBSCRIBE FAILED NO PROD FOUND")
        return -1

    print("SUBSCRIBE WORKED")

def unsubscribe(prod_id, sub_id, sub_address_and_port):
    # TODO implement unsubscribe + error checking for sub_id / prod_id
    # TODO I have to check sub_id exists, prod_id exists, and that sub is subscribed to prod, and prod has sub as a subscriber

    print("unsubscribe called")
    # Check sub exists in our list
    sub_found = False
    for sub in subscribers_list:
        print(sub.sub_id + " " + sub_id)
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
    
    print("I think unsubscribed")


while(True):
    # breaking up the header and payload
    message, address = broker_socket.recvfrom(bufferSize)
    header_length = message[:2]
    header_length_as_int = int(header_length)
    header = message[:header_length_as_int]

    message_as_string = message.decode()
    print(message_as_string)
    packet_request_type = header.decode()[2]


    if packet_request_type == "S": #example message = 03SP01S01
        prod_id = message_as_string[header_length_as_int:][:3]
        sub_id = message_as_string[header_length_as_int:][3:6]
        subscribe(prod_id, sub_id, address)

    elif packet_request_type == "P": # packet
        prod_id_last_digit = message_as_string[header_length_as_int-1] # header length as int would take the last digit of the prod id. e.g. 06PP01, headerlengthasint = 6. 
        print(len(producers_list[0].subs_list))
        for subscriber in producers_list[int(prod_id_last_digit)-1].subs_list:
            # print("Broker sent msg! ")
            broker_socket.sendto(message, subscriber.sub_address_and_port)

    elif packet_request_type == "U":
        prod_id = message_as_string[header_length_as_int:][:3]
        sub_id = message_as_string[header_length_as_int:][3:6]
        unsubscribe(prod_id, sub_id, address)





