#!/usr/local/bin/python3
#############################################################################
# AUTHOR: Jorel Paddick 
# FILE: deamon_services.py
# CREATED: 31-01-2019
# MODIFIED: 
# PURPOSE: 
#############################################################################
import subprocess

class Process(object):
    def __init__(self, pid, tty, time, cmd):
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd

def read_process_list(filename):
    with open(filename, 'r') as plist:
        print("This will not work")

def obtain_process_list(output):
    filename = output + "psout"
    with open(filename, 'w') as outfile:
        subprocess.Popen(["ps", "-A"], stdout=outfile)
        outfile.close()
    read_process_list(filename)

def main(outdir):
    obtain_process_list(outdir)

if __name__ == "__main__":
    # main()
    pass