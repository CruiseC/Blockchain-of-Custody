import struct
import os
import sys
import hashlib
import uuid
from collections import namedtuple
from datetime import datetime
from errors import *

def addition(case_id, item_id, handler, organization, file_path):
    
    success = ''
    print_case = 0

    orig_case = case_id

    case_id = case_id.replace("-", "")
    rev_case_id = ""

    for i in range(0, len(case_id), 2):
        rev_case_id = case_id[i]+case_id[i+1] + rev_case_id
        

    case_id = rev_case_id


    try:
        filepath = open(file_path, "rb")
        filepath.close()
    except:

        block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
        block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
        block_data = namedtuple('Block_Data', 'data')

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

    filepath = open(file_path, 'rb')

    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')

    prev_hash = ''
    prev_id = []

    while True:
        try:

            head_cont = filepath.read(block_format_head.size)
            curr_head = block_head._make(block_format_head.unpack(head_cont))
            prev_id.append(curr_head.item_id)
            block_data_format = struct.Struct(str(curr_head.length) + 's')
            data_cont = filepath.read(curr_head.length)
            curr_data = block_data._make(block_data_format.unpack(data_cont))



            prev_hash = hashlib.sha1(head_cont + data_cont).digest()

        except:

            #print("final block")
            break


    for i in item_id:


        if int(i) in prev_id:
            print("errror duplicate")
            sys.exit(1)

        if not print_case:
            print("Case: ", orig_case)
            print_case += 1

        currTime = datetime.now()

        #take out organization and turn it into a string
        organ = organization[0]

        timestamp = datetime.timestamp(currTime)
        headVals = (prev_hash, timestamp, uuid.UUID(case_id).bytes, int(i), str.encode("CHECKEDIN"), handler.encode(), organ.encode(), 0)
        dataVal = b''
        block_data_format = struct.Struct('0s')
        packed_headVals = block_format_head.pack(*headVals)
        packed_dataVals = block_data_format.pack(dataVal)
        curr_head = block_head._make(block_format_head.unpack(packed_headVals))
        curr_data = block_data._make(block_data_format.unpack(packed_dataVals))

        prev_hash = hashlib.sha1(packed_headVals + packed_dataVals).digest()


        filepath = open(file_path, 'wb')
        filepath.write(packed_headVals)
        filepath.write(packed_dataVals)
        filepath.close()

        print("Added item:", i)
        print("\tStatus: CHECKEDIN")
        print("\tTime of action:", currTime.strftime(
            '%Y-%m-%dT%H:%M:%S.%f') + 'Z')


        success = True

    if success:
        return True
    else:
        return False