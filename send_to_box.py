#!/usr/bin/env python3
'''
    Author: Jay Spendlove
    email: jayclark24@gmail.com
    Purpose of script: Automatically send files to box for storage, and 
    delete the file if uploaded correctly, or log if not uploaded correctly
    **NOTE: This script implements a send_to_box CLASS versus straight script
    as in auto_send_to_box.py**

TODO:
    -gitignore- get private info off of github
    -combine confic_auth_args and authentication functions
    -get rid of access token?

'''

import os, sys, logging, datetime, json, cProfile
from os import path
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException

def check_arguments():
    '''
    check if command line argument for file name was inputted correctly.
    raises exception for any error
    '''
    if len(sys.argv) < 2:
        raise ValueError("Additional argument needed in command line--file name")
    check_file_exists(sys.argv[1])
    if len(sys.argv) > 2:
        check_file_exists(sys.argv[2])

def check_file_exists(file_name):
    '''
    checks to make sure file name exists in given directory
    raises exception if file does not exist
    '''
    if not path.exists(file_name):
        raise FileNotFoundError ("File chosen for upload does not exist in this directory")

class SendToBox (object):

    def __init__(self, config_filename='config.json'):
        self.client = None
        self.config_filename = config_filename
        self.authenticate()

    def authenticate (self):
        '''
        JWT authentication
        '''
        auth = JWTAuth.from_settings_file(self.config_filename)
        access_token = auth.authenticate_instance()
        self.client = Client(auth)

    def upload_file(self, filename):
        '''
        using a try will attempt to upload file to box. If successful, will delete the file
        from local system. If unsuccessful, will log error message to log file and 
        NOT delete the file
        '''
        try:
            box_file = self.client.folder('0').upload(filename, preflight_check = True)
            os.remove(filename)
        except BoxAPIException as err:
            self.log_failure(filename, err)
    
    def log_failure(self, file_name, err):
        log_file_name = "failed_uploads.log"
        logging.basicConfig(filename=log_file_name, level=logging.ERROR)
        l1=logging.getLogger(file_name)
        l1.error(f"File failed to upload:\n {err}\n")

        return

if __name__ == "__main__":
    check_arguments()
    if len(sys.argv) > 2:
        s1 = SendToBox(sys.argv[2])
    else:
        s1 = SendToBox()
    s1.upload_file(sys.argv[1])
