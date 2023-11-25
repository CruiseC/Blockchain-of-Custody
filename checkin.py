import struct
import os
import uuid
import hashlib  
from collections import namedtuple
from datetime import datetime
from errors import *
from initialize import initialize 

def checkin(item_id, file_path):
    success = True
    state = ' '
    previousHash = 'b'
    case_id = ' '
    
    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')
    
    to_initialize = initialize(file_path)
        
    filepath = open(file_path, 'rb')
    
    while True:
        
        try:
            head_contents = filepath.read(block_format_head.size)
            curr_head = block_head._make(
                block_format_head.unpack_head_contents))
            block_data_format = struct.Struct(
                str(curr_head.length)+'s')
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
