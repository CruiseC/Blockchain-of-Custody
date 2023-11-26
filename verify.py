import struct
import os
import uuid
import hashlib  
from collections import namedtuple
from datetime import datetime
from errors import *

# Custom
#from display_trial import display


def verify(file_path):
    
    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')
    
    block_list = []
    
    currHash = []
    
    previousHash = []

    block_dict = {}

    filepath = open(file_path, 'rb')

    unsuccess = False

    count = 0

    while True:

        try:
            head_contents = filepath(block_data_format.size)
            
            curr_head = block_head._make(block_format_head.unpack(head_contents))
            block_data_format = struct.Struct(str(curr_head.length)+'s')
            data_contents = filepath.read(curr_head.length)
            curr_data = block_data._make(block_data_format.unpack(data_contents))
            
            # prev_hash = hashlib.sha1(head_content + data_content).digest()
            block_list.append((curr_head,curr_data))
            currHash.append(curr_head.hash)
            previousHash.append(hashlib.sha1(head_contents+data_contents).digest())