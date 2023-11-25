import struct
import os
import uuid
import hashlib  
from collections import namedtuple
from datetime import datetime
from errors import *

def checkout(item_id, file_path):

    success = True
    state = ''
    previousHash = b''
    case_id = ''

    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')

    filepath = open(file_path, 'rb')

    while True:

        try:
            head_contents = filepath.read(block_format_head.size)
            curr_head = block_head._make(
                block_format_head.unpack(head_contents))
            block_data_format = struct.Struct(str(curr_head.length)+'s')
            data_contents = filepath.read(curr_head.length)
            curr_data = block_data._make(
                block_data_format.unpack(data_contents))
            
            previousHash = hashlib.sha1(head_contents+data_contents).digest()

            if int(item_id[0]) == curr_head.item_id:
                case_id = curr_head.case_id
                state = curr_head.state

        except:
            break

    filepath.close()

    try:

        if state.decode('utf-8').rstrip('\x00') == "CHECKEDOUT":

            currTime = datetime.now()
            timestamp = datetime.timestamp(currTime)
            headVals = (previousHash, timestamp, case_id, int(item_id[0]), str.encode("CHECKEDIN"), 0)
            dataVals = b''
            block_data_format = struct.Struct('0s')
            packed_headVals = block_format_head.pack(*headVals)
            packed_dataVals = block_data_format.pack(dataVals)
            curr_head = block_head._make(
                block_format_head.unpack(packed_headVals))
            curr_data = block_data._make(
                block_data_format.unpack(packed_dataVals))
            
            print(curr_head)
            print(curr_data)
            
            filepath = open(file_path, 'ab')
            filepath.write(packed_headVals)
            filepath.write(packed_dataVals)
            filepath.close()

            print("Case:", str(uuid.UUID(bytes=case_id)))
            print("Checked in item:", item_id[0])
            print("\tStatus:", "CHECKEDOUT")
            print("\tTime of action:", currTime.strftime(
                '%Y-%m-%dT%H:%M:%S.%f') + 'Z')

            success = True
        
        else:
            Incorrect_State()

    except:
        # Item ID not found
        Item_Not_Found()
        
    sys.exit(0)