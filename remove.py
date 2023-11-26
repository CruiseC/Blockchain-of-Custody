import os
import struct
import sys
import argparse
import hashlib

from collections import namedtuple
from datetime import datetime
from errors import *

# Prevents any further action from being taken on the evidence item 
# specified. The specified item must have a state of CHECKEDIN for 
# the action to succeed.

def remove(item_id, reason, owner, file_path):

    case_id = ''
    state = ''
    prev_hash = b''

    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')

    file_path = open(file_path, 'rb')
    # print("1")

    while True:
        try: 
            # print("2")
            head = file_path.read(block_format_head.size)
            current_head = block_head._make(block_format_head.unpack(head))
            data_format = struct.Struct(str(current_head.length) + 's')
            data_content = file_path.read(current_head.length)
            current_block_data = block_data._make(data_format.unpack(data_content))
            prev_hash = hashlib.sha1(head+data_content).digest()

            if int(item_id[0]) == current_head.item_id:
                
                case_id = current_head.case_id
                state = current_head.state
                handler = current_head.handler
                orginization = current_head.organization
        
        except: 
            break

    file_path.close()

    try: 
        # print("3.1")
        if state.decode('utf-8').rstrip('\x00') == "CHECKEDIN":
            # print("3")
            current_time = datetime.now()
            time_stamp = datetime.timestamp(current_time)

            if owner: 
                data_value = " ".join(owner)
                head_values = (prev_hash, time_stamp, case_id, int(item_id[0]), str.encode(reason), str.encode(""), str.encode(""), 0)
                data_format = struct.Struct(str(len(data_value)+1)+'s')
                packed_data_Vals = data_format.pack(str.encode(data_value))
                # print("b4")

            else:

                head_values = (prev_hash, time_stamp, case_id, int(item_id[0]), str.encode(reason), str.encode(""), str.encode(""), 0)
                data_format = struct.Struct('0s')
                data_value = b''
                packed_data_Vals = data_format.pack(data_value)
            # print("4")
            packed_head_Vals = block_format_head.pack(*head_values)
            # print("5")
            current_head = block_head._make(block_format_head.unpack(packed_head_Vals))
            current_block_data = block_data._make(data_format.unpack(packed_data_Vals))
            

            file_path = open(file_path.name, 'ab')
            # print("6")
            file_path.write(packed_head_Vals)
            file_path.write(packed_data_Vals)
            file_path.close()

            print("Removed item:", str(item_id[0]))
            print("\tStatus:", reason)
            print("\tOwner info:", data_value)
            print("\tTime of Action:", current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z')

            success = True
        
        else:
            print("Item is not Checked In")
            Initial_Block_Error()

    except:
        Initial_Block_Error()