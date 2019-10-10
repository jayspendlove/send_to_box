#!/usr/bin/python3
'''
    Author: Jay Spendlove
    email: jayclark24@gmail.com
    Purpose of script: take command line argument of files to be sent to
    BOX, and send corresponding file to BOX.

if __name__ == "__main__"
**makes sure the script is only executed when the file itself is called, not when imported

sys.argv[1]
**holds the command line options, index 1 references option for file to be uploaded (e.g. "t2.txt")
**python3 send_to_box.py "t1.txt"

Checks for input errors from user (no file input, file does not exist)

TODO:
- generate test files 
- Change process of authorizing code so that user input is not required, we want to hard code it
- try making new app in box, with different authentication method

'''
import sys
from os import path
from boxsdk import Client,JWTAuth
import json


if __name__ == "__main__":
    config_args = None
    with open('config.json') as f:
       config_args = json.load(f)

    auth = JWTAuth(**config_args)
    access_token = auth.authenticate_instance()

    '''check that file name argument has been given in command line'''
    if len(sys.argv) < 2:
        raise ValueError("Additional argument needed in command line--file name")
    file_name= sys.argv[1]

    '''check that argument given is a file in given directory'''
    if not path.exists(file_name):
        raise FileNotFoundError ("File chosen for upload does not exist in this directory")
    file_path = "/home/jay/Documents/Codes/GB/send_to_box/" + file_name 

    client = Client(auth)

    '''option for folder function is the folder ID for 'test_GB_file_uploads' in Box'''
    folder_id = '88895453960'
    client.folder('0').upload(file_path)

    '''this line of code can be used to get the folder ID of folder in the root folder'''
    #print(client.folder('0').get())
