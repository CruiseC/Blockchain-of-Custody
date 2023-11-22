import struct
import os
import sys
import argparse
from collections import namedtuple
from datetime import datetime
from errors import *


def initialize(file_path):


    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')
    

    try: 
        filepath = open(file_path, "rb")
        filepath.close()
    except:

        currTime = datetime.now()
        timestamp = datetime.timestamp(currTime)
        headVals = (str.encode(""), timestamp, str.encode(""), 0, str.encode("INITIAL"), str.encode(""), str.encode(""), 14)
        dataVal = (str.encode("Initial block"))
        block_data_format = struct.Struct('14s')
        packed_headVals = block_format_head.pack(*headVals)
        packed_dataVals = block_data_format.pack(dataVal)

        curr_head = block_head._make(block_format_head.unpack(packed_headVals))
        curr_data = block_data._make(block_data_format.unpack(packed_dataVals))

        print(curr_head)
        print(curr_data)
        print("This went thourhg initlaize path and printed")

        filepath = open(file_path, 'wb')
        filepath.write(packed_headVals)
        filepath.write(packed_dataVals)
        filepath.close()

    filepath = open(file_path, 'rb')

    try:
        head_contents = filepath.read(block_format_head.size)
        curr_head = block_head._make(block_format_head.unpack(head_contents))
        block_data_format = struct.Struct(str(curr_head.length) + 's')
        data_contents = filepath.read(curr_head.length)
        curr_data = block_data._make(block_data_format.unpack(data_contents))

    except:
        print("Blockchain file not found.")
        
        Initial_Block_Error

    filepath.close()

    if "INITIAL" in (curr_head.state).decode('utf-8').upper():
        return False
    else:
        return True

