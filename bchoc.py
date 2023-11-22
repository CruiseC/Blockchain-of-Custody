import hashlib 
import argparse
import struct
import os


parser = argparse.ArgumentParser(description="Create Blockchain of Custody form")
parser.add_argument("action")
parser.add_argument('-c', help='case id') #case ID
parser.add_argument('-i', action='append') #Item ID
parser.add_argument('-h') #handler 
parser.add_argument('-o') #organization
parser.add_argument('-n') #number of entries
parser.add_argument('-y', '-why') #reason
parser.add_argument('-o', nargs='*') #owner Info

args = parser.parse_args()
action = args.action

