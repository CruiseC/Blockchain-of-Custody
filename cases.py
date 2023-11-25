import struct
import hashlib
import os
import uuid

from datetime import datetime
from collections import namedtuple


def cases(file_path):




    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')

    blocks = []

    filepath = open(file_path, 'rb')


    while True:
        try: 
            head_cont = filepath.read(block_format_head.size)
            curr_head = block_head._make(block_format_head.unpack(head_cont))
            block_data_format = struct.Struct(str(curr_head.length) + 's')
            data_cont = filepath.read(curr_head.length)
            curr_data = block_data._make(block_data_format.unpack(data_cont))

            blocks.append((curr_head, curr_data))

        except:
            break


    filepath.close()


    for block in blocks:
        caseID = b""

        rev_case_id = block[0].case_id

        for j in range(0, len(rev_case_id)):
            caseID = bytes([rev_case_id[j]]) + caseID


        print(uuid.UUID(bytes=caseID))
        