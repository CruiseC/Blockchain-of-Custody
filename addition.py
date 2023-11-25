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

    case_id = case_id.replace("-", "")
    rev_case_id = ""

    for i in range(0, len(case_id), 2):
        rev_case_id = case_id[i]+case_id[i+1] + rev_case_id

    case_id = rev_case_id