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

            if str(uuid.UUID(bytes=curr_head.case_id)) in block_dict:
                if curr_head.item_id in block_dict[str(uuid.UUID(bytes=curr_head.case_id))].keys():
                    
                    last_state = block_dict[str(uuid.UUID(bytes=curr_head.case_id))][curr_head.item_id]
                    current_state = (curr_head.state.decode()).rstrip('\x00')

                    if current_state == "CHECKEDIN":
                        if last_state != "CHEKEDOUT":
                            unsuccess = True
                            break

                    elif current_state == "CHECKEDOUT":
                        if last_state != "CHEKEDIN":
                            unsuccess = True
                            break

                    elif current_state == ["RELEASED", "DESTROYED", "DISPOSED"]:
                        if last_state != "CHEKEDIN":
                            unsuccess = True
                            break
                        if last_state == "RELEASED":
                            if not curr_head.length:
                                unsuccess = True
                                break

                    block_dict[str(uuid.UUID(bytes=curr_head.case_id))][curr_head.item_id] = (curr_head.state.decode()).rstrip('\x00')

                    pass

                else: 

                    if (curr_head.state.decode()).rstrip('\x00') in ["RELEASED", "DESTROYED", "DISPOSED"]:
                        unsuccess = True
                        break

                    if not (curr_head.state.decode()).rstrip('\x00') == "CHECKEDIN":
                        unsuccess = True
                        break

                block_dict[str(uuid.UUID(bytes=curr_head.case_id))][curr_head.item_id] = (curr_head.state.decode()).rstrip('\x00')

            else: 
                    if (curr_head.state.decode()).rstrip('\x00') in ["RELEASED", "DESTROYED", "DISPOSED"]:
                        unsuccess = True
                        break

                    block_dict[str(uuid.UUID(bytes=curr_head.case_id))] = {}
                    block_dict[str(uuid.UUID(bytes=curr_head.case_id))][curr_head.item_id] = (curr_head.state.decode()).rstrip('\x00')

            count = count + 1

        except:

            if not count:
                unsuccess = True
                break

            if len(head_contents):
                Invalid_Block()
                unsuccess = True
                break

            break

    filepath.close()

    if unsuccess:
        Invalid_Chain()

    if len(currHash) != len(set(currHash)):
        Duplicate_Hashes()

    print(block_list)
    print()

    if previousHash[:-1] != currHash[1:]:
        Invalid_Chain()

