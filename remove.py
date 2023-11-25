import os
import struct
import sys
import argparse

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

    while True:
        try: 

            head = file_path.read(block_format_head.size)
            current_head = block_head._make(block_format_head.unpack(head))
            data_format = struct.Struct(str(current_head.length) + 's')
            data_content = file_path.read(current_head.length)
            current_block_data = block_data._make(block_format_head.unpack(data_content))
            prev_hash = hashlib.sha1(head+data_content).digest()

            if int(item_id[0]) == current_head.item_id:
                case_id = current_head.case_id
                state = current_head.state
        
        except: 
            break


    file_path.close()

    try: 

        if state.decode('utf-8').rstrip('\x00') == "CHECKEDIN":

            current_time = datetime.now()
            time_stamp = datetime.timestamp(current_time)

            if owner: 

                data_value = " ".join(owner)
                head_values = (prev_hash, time_stamp, case_id, item_id, int(item_id[0]), str.encode(reason), handler, orginization, 0)

                data_format = struct.Struct(str(len(data_value)+1)+'s')

                print(str(len(owner)) + 's', data_value, len(data_value))

                packed_dataVals = block_data_format.pack(str.encode(data_value))

            else:

                head_values = head_values = (prev_hash, time_stamp, case_id, item_id, int(item_id[0]), str.encode(reason), handler, orginization, 0)
                block_data_format = struct.Struct('0s')
                data_value = b''
                packed_dataVals = block_data_format.pack(data_value)

            packed_headVals = block_format_head.pack(*head_values)

            current_head = block_head._make(block_format_head.unpack(packed_headVals))
            current_block_data = block_data._make(block_data_format.unpack(packed_dataVals))

            file_path = open(file_path, 'ab')
            file_path.write(packed_headVals)
            file_path.write(packed_dataVals)
            file_path.close()

            print("Removed item:", item_id[0])
            print("\tStatus:", reason)
            print("\tOwner info:", data_value)
            print("\tTime of Action:", current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z')

            success = True
        
        else:
            print("Item is not Checked In")
            Initial_Block_Error()

    except:
        Initial_Block_Error()

    sys.exit(0)
