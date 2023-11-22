import hashlib 
import argparse
import struct
import os
from collections import namedtuple   
import uuid


parser = argparse.ArgumentParser(description="Create Blockchain of Custody form")
# action = {add, checkout, checkin, show cases, show items, show history, remove, init, verify}
parser.add_argument("action")
parser.add_argument('-c', help='case id') #case ID
parser.add_argument('-i', action='append') #Item ID
#parser.add_argument('-h') #handler  #having trouble with this due to '-h" also being help feature for arg parse
#parser.add_argument('-o') #organization # cant have two arguments that are '-o' need to find workaround
parser.add_argument('-n') #number of entries
parser.add_argument('-y', '-why') #reason
parser.add_argument('-o', nargs='*') #owner Info

args = parser.parse_args()
action = args.action
arguments = {}



#file_path = os.getenv('BCHOC_FILE_PATH')
file_path = "chain"


block_format = struct.Struct('32s d 16s I 12s 20s 20s I')
block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
block_data = namedtuple('Block_Data', 'data')
prev_hash = b''

#Test for arugment parsing correctly
if action not in ["init", "verify"]:


    if action == "add":
        print("add")

    elif action == "checkout" or action == "checkin":
        print ("checkout/checkin")

    elif action == "show cases":
        #not working yet need to figure out way to go into this path with double letter arguments
        print("cases showing")


    elif action == "show items":
        #not working yet need to figure out way to go into this path with double letter arguments
        print("show items")

    elif action == "show history":
        #not working yet need to figure out way to go into this path with double letter arguments
        print("history")

    else: 
        print("remove")

else:
    if action == "init":
        print("init")

    else:
        #verify
        print("verify")

