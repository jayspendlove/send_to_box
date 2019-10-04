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
- in binary??
- do I have to open the file to send it?
- access folder id of not the root
- test for zip file
- stupid proof it
    *No command line options "No file indicated"
    *file not valid
- generate test files 


'''
import sys
from boxsdk import DevelopmentClient

if __name__ == "__main__":
    file_name= sys.argv[1]
    path = "/home/jay/Documents/Codes/GB/" + file_name 
    client = DevelopmentClient()

    '''option for folder function is the folder ID for 'test_GB_file_uploads' in Box'''
    client.folder('88895453960').upload(path)

    '''this line of code can be used to get the folder ID of folder in the root folder
    client.folder('0').get()
    '''
