import hashlib 
import argparse
import struct
import os
from collections import namedtuple   
import uuid
import sys
from datetime import datetime

from initialize import initialize
from addition import addition
from history import history
from cases import cases
from checkin import checkin
from checkout import checkout
from remove import remove

parser = argparse.ArgumentParser(description="Create Blockchain of Custody form", add_help=False, conflict_handler='resolve')
# action = {add, checkout, checkin, show cases, show items, show history, remove, init, verify}
parser.add_argument("action")
parser.add_argument("shows", nargs='?')
parser.add_argument('-c', help='case id') #case ID
parser.add_argument('-i', action='append') #Item ID
parser.add_argument('-h') #handler  
parser.add_argument('-o') #organization 
parser.add_argument('-n') #number of entries
parser.add_argument('-y', '-why') #reason
parser.add_argument('-o', nargs='*') #owner Info

args = parser.parse_args()
action = args.action
shows = args.shows
arguments = {}



#file_path = os.getenv('BCHOC_FILE_PATH')
file_path = "Blockchain"


block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
block_data = namedtuple('Block_Data', 'data')
prev_hash = b''

#Test for arugment parsing correctly
if action not in ["init", "verify"]:


    if action == "add":

        #place arguments from commandline to lists
        arguments["case_id"] = args.c
        arguments["item_id"] = args.i 
        arguments["handler"] = args.h 
        arguments["organization"] = args.o 
        if arguments["case_id"] and arguments["item_id"]:
            addition(arguments["case_id"], arguments["item_id"], arguments["handler"], arguments["organization"], file_path)

        else:
            print("arguments error")
        #print("add")

    elif action == "checkout" or action == "checkin":

        arguments["item_id"] = args.i
        arguments["handler"] = args.h 
        arguments["organization"] = args.o 

        if action == 'checkin':
            checkin(arguments['item_id'], arguments["handler"], arguments["organization"], file_path)
        else:
            checkout(arguments['item_id'], arguments["handler"], arguments["organization"], file_path)

    #show cases function
    elif action == "show" and shows == "cases":
        cases(file_path)

    elif action == "show" and shows == "items":
        
        print("show items")

    elif action == "show" and shows == "history":
        arguments["case_id"] = args.c
        arguments["item_id"] = args.i
        arguments["number"] = args.n

        history(arguments["case_id"], arguments["item_id"], arguments["number"], file_path)

    else: 
        print("remove")
        # initialize arguments from the command line into the arguments array 
        arguments["item_id"] = args.i 
        arguments["reason"] = args.y
        arguments["owner"] = args.o 

        if (arguments["reason"] == "RELEASED"):
            if not arguments["owner"]:
                print("error") # replace with error handling
        
        if arguments["reason"] not in ["RELEASED", "DISPOSED", "DESTROYED"]:
            print("error")  # replace with error handling

        # pass arguments into the remove function
        remove(arguments["item_id"], arguments["reason"], arguments["owner"], file_path)

else:
    if action == "init":

        initiate = initialize(file_path)
        
        
        if initiate == True:
            print("Blockchain file found with INITIAL block.")

            #exit
            sys.exit(0)
        else:
            currTime = datetime.now()
            timestamp = datetime.timestamp(currTime)
            headVals = (str.encode(""), timestamp, str.encode(""), 0, str.encode("INITIAL"), str.encode(""), str.encode(""), 14)
            dataVal = (str.encode("Initial block"))
            block_data_format = struct.Struct('14s')
            packed_headVals = block_format_head.pack(*headVals)
            packed_dataVals = block_data_format.pack(dataVal)

            curr_head = block_head._make(block_format_head.unpack(packed_headVals))
            curr_data = block_data._make(block_data_format.unpack(packed_dataVals))

            #print(curr_head)
            #print(curr_data)
            print("Blockchain file not found. Created INITIAL block.")

            filepath = open(file_path, 'wb')
            filepath.write(packed_headVals)
            filepath.write(packed_dataVals)
            filepath.close()

            #intializeinbkod
            prev_hash = hashlib.sha1(packed_headVals + packed_dataVals).digest()

    else:
        #verify
        print("verify")

sys.exit(0)
