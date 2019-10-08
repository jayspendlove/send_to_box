#!usr/bin/env python3
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

TODO:
- test for zip file
- generate test files 


'''
import sys
import os.path
from os import path
from boxsdk import DevelopmentClient

if __name__ == "__main__":
    '''check that file name argument has been given in command line'''
    if(len(sys.argv) < 2):
        raise ValueError("Additional argument needed in command line--file name")
    file_name= sys.argv[1]

    '''check that argument given is a file in given directory'''
    if (path.exists(file_name) == False):
        raise FileNotFoundError ("File chosen for upload does not exist in this directory")
    file_path = "/home/jay/Documents/Codes/GB/send_to_box/" + file_name 
    client = DevelopmentClient()

    '''option for folder function is the folder ID for 'test_GB_file_uploads' in Box'''
    folder_id = '88895453960'
    client.folder(folder_id).upload(file_path)

    '''this line of code can be used to get the folder ID of folder in the root folder
    client.folder('0').get()
    '''
