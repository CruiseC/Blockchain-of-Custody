import struct
import os
import uuid
import hashlib  
from collections import namedtuple
from datetime import datetime
from errors import *
from initialize import initialize 

def checkin(item_id, handler, organization, file_path):
    success = True
    state = ''
    previousHash = b''
    case_id = ''

    #store organization in string for encode
    organ = organization[0]
    

    
    block_format_head = struct.Struct('32s d 16s I 12s 20s 20s I')
    block_head = namedtuple('Block_head', 'hash timestamp case_id item_id state handler organization length')
    block_data = namedtuple('Block_Data', 'data')
    
    intiate = initialize(file_path)
        
    filepath = open(file_path, 'rb')
    
    while True:
        
        try:
            head_contents = filepath.read(block_format_head.size)
            curr_head = block_head._make(block_format_head.unpack(head_contents))
            block_data_format = struct.Struct(str(curr_head.length)+'s')
            data_contents = filepath.read(curr_head.length)
            curr_data = block_data._make(block_data_format.unpack(data_contents))
            
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
            headVals = (previousHash, timestamp, case_id, int(item_id[0]), str.encode("CHECKEDIN"), handler.encode(), organ.encode(), 0)
            dataVals = b''
            block_data_format = struct.Struct('0s')
            packed_headVals = block_format_head.pack(*headVals)
            packed_dataVals = block_data_format.pack(dataVals)
            curr_head = block_head._make(block_format_head.unpack(packed_headVals))
            curr_data = block_data._make(block_data_format.unpack(packed_dataVals))
            
            #print(curr_head)
            #print(curr_data)
            
            filepath = open(file_path, 'ab')
            filepath.write(packed_headVals)
            filepath.write(packed_dataVals)
            filepath.close()

            caseID = b""
        
            rev_case_id = case_id

            for j in range(0, len(rev_case_id)):
                caseID = bytes([rev_case_id[j]]) + caseID

            print("Case:", str(uuid.UUID(bytes=caseID)))
            print("Checked in item:", item_id[0])
            print("\tStatus:", "CHECKEDIN")
            print("\tTime of action:", currTime.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z')

            success = True
        
        else:
            print('Incorrect State')
            sys.exit(1)
            

    except:
        # Item ID not found
        print('incorrect Item')
        sys.exit(1)
        
        
    sys.exit(0)
