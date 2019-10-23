#!/usr/bin/env python3
'''
    Author: Jay Spendlove
    email: jayclark24@gmail.com
    Purpose of script: Automatically send files to box for storage, and 
    delete the file if uploaded correctly, or log if not uploaded correctly
    **NOTE: This script implements a send_to_box CLASS versus straight script
    as in auto_send_to_box.py**
'''

import os, sys, logging, datetime, json, cProfile
from os import path
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException

class SendToBox (object):
    client = None
    file_name = None
    file_path = None

    def upload_file(self):
        '''
        function that puts together all the individual functions to successfully 
        upload file
        '''
        #log = self.config_log_file()
        auth_args = self.config_authentication_args()
        authorization = self.authenticate(auth_args)
        file_name = self.check_arguments()
        self.check_file_exists(file_name)
        client, file_path = self.prepare_for_upload(authorization, file_name)
        status = self.ensure_successful_upload(client, file_name, file_path)

        return status

    def config_log_file(self):
        '''
        DOES NOT WORK RIGHT NOW, ADVANCED IMPLEMENTATION OF log_failure
        function to configure a log file
        '''
        formatter=logging.Formatter('%(asctime)s [%(levelname)]%(message)s, datefmt="%m/%d/%y %H:%M:%S"')
        fh = logging.FileHandler('a_failed_uploads.log')
        fh.setFormatter(formatter)
        logging.getLogger().addHandler(fh)
        logging.getLogger().setLevel(logging.ERROR)

        return logging

    def config_authentication_args (self):
        '''
        get configuration arguments from config.json for use in authentication process
        returns configuration arguments for authentication
        '''
        config_args = None
        config_args = JWTAuth.from_settings_file('/home/jay/Documents/Codes/GB/send_to_box/new_config.json')
        #with open('config.json') as f:
            #config_args = json.load(f)

        return config_args

    def authenticate (self, auth_args):
        '''
        authenticate in preparation for file upload
        returns authorization information
        '''
        #auth = JWTAuth(**auth_args)
        auth = auth_args
        access_token = auth.authenticate_instance()
        return auth

    def check_arguments(self):
        '''
        check if command line argument for file name was inputted correctly.
        Returns file name if correct, Will raise exception if not.
        '''
        if len(sys.argv) < 2:
            raise ValueError("Additional argument needed in command line--file name")
        f_name= sys.argv[1]
        return f_name

    def check_file_exists(self, file_name):
        '''
        checks to make sure file name exists in given directory
        returns True if file exists, raises exception if not
        '''
        if not path.exists(file_name):
            raise FileNotFoundError ("File chosen for upload does not exist in this directory")
        return True

    def prepare_for_upload(self, authorization, file_name):
        '''
        prepares for upload by declaring Client object and putting value in 
        file_name variable
        Returns file_path
        '''
        client = Client(authorization)
        f_path = "/home/jay/Documents/Codes/GB/send_to_box/" + file_name
        return client,f_path

    def ensure_successful_upload(self, client, file_name, file_path):
        '''
        using a try will attempt to upload file to box. If successful, will delete the file
        from local system. If unsuccessful, will log error message to log file and 
        NOT delete the file
        returns True or False based on status of upload
        '''
        try:
            print("THis works right?")
            box_file = client.folder('0').upload(file_path, preflight_check = True)
            print("but will this?")
        except BoxAPIException:
            print("aha!")
            self.log_failure(file_name)
            #return False
            pass
        else:
            os.remove(file_path)
            #return True
    
    def log_failure(self, file_name):
        log_file_name = "failed_uploads.log"
        logging.basicConfig(filename=log_file_name, level=logging.ERROR)
        l1=logging.getLogger(file_name)

        return

if __name__ == "__main__":
    s1 = SendToBox()
    s1.upload_file()
