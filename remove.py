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

    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')

    file_path = open(file_path, 'rb')

    while True:

        head = file_path.read(block_format_head.size)
        current_head = block_head._make(block_format_head.unpack(head))
        data_format = struct.Struct(str(current_head.length))
        data_content = file_path.read(current_head.length)
        current_block_data = block_data._make(block_format_head.unpack(data_content))
        prev_hash = hashlib.sha1(head+data_content).digest()

        if int(item_id[0]) == current_head.item_id:
            case_id = current_head.case_id
            state = current_head.state


    file_path.close()