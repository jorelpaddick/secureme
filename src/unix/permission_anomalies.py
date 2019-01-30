#!/usr/local/bin/python3
"""
This module aims to search the UNIX filesystem hierarchy for 
files and directories with permissions that are 'out of place'.
For example, globally writable files which should not be writable or 
files such as /etc/shadow which should not even be readable (except by root).
This module will also check for invalid GUID and SUID permission settings.
"""
from utils.termout import *
import os
import stat

def check_mode(file, expected_mode):
    """
    Check the 'file' for 'expected_mode' expected permissions)
    as an octal value '0000'
    """
    full_perms = oct(os.stat(file)[0])
    mode = full_perms[-4:] 
    print_info("Mode for " + file + ": " + mode)
    print_info("^[" + full_perms + "]")
    correct = True
    if(mode != expected_mode):
        print_warning("Permissions invalid for " + file + "!")
        correct = False
    else:
        print_ok("Permissions for " + file + " are good")
    return correct

def check_etc():
    PASSWD = "/etc/passwd"
    SHADOW = "/etc/shadow"
    if(check_mode(PASSWD, "0644") == False):
        print_critical("/etc/passwd FILE PERMISSIONS INCORRECT!")
    # if(check_file(SHADOW, "0644") == False):
    #     print_critical("/etc/shadow FILE PERMISSIONS INCORRECT!") 
    # this is linux specific

def main(outdir):
    set_logging(outdir + "permissions.log")
    print_title("UNIX Permission Check")
    print_subtitle("Created by Jorel Paddick\n")
    check_etc()

if __name__ == "__main__":
    main("./")
    