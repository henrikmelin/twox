import dropbox
import sys
import os
import argparse

# Get the local and remote files from the command line args
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
args = parser.parse_args()

if (args.input is None or args.output is None) : 
    print('Usage: pyhon3 upload2dropbox.py --input locafile.jpg --output /remote/path/file.jpg')
    exit()
    
# Get the token exported in .bashrc
access_token = os.getenv('DROPBOX_ACCESS_TOKEN')

# Upload the file
print('Uploading ' + args.output)
dbx = dropbox.Dropbox(access_token)
with open(args.input, 'rb') as f:
    dbx.files_upload(f.read(), args.output)


