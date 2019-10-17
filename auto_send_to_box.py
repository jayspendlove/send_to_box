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
-test with script that calls this script

'''
import sys
import os
from os import path
from boxsdk import Client,JWTAuth
from boxsdk.exception import BoxAPIException
import json
import logging
import datetime

if __name__ == "__main__":
    now = datetime.datetime.now()
    log_file_name= now.strftime("%d-%m-%Y_") + "failed_uploads.log"
    #log_file_name= "failed_uploads.log"
    '''for logging upload failures'''
    #FORMAT = '%now.strftime("%Y-%m-%d_%H:%M) %(message)s'
    logging.basicConfig(filename=log_file_name, level=logging.ERROR)

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

    '''option for folder function is the folder ID for 'auto_send_to_box' in Box'''
    
    try:
        box_file = client.folder('0').upload(file_path, preflight_check = True)
    except BoxAPIException :
        l1=logging.getLogger(file_name)
        l1.error('File did not upload to box.')
        #print("Upload failure /exception data to .log file")
        pass
    else:
        os.remove(file_path)
    

    '''this line of code can be used to get the folder ID of folder in the root folder'''
    #print(client.folder('0').get())
