#!/usr/local/bin/python3
"""
This module aims to search the UNIX filesystem hierarchy for 
files and directories with permissions that are 'out of place'.
For example, globally writable files which should not be writable or 
files such as /etc/shadow which should not even be readable (except by root).
This module will also check for invalid GUID and SUID permission settings.
"""
from utils.termout import *
import os # Required to check file modes
import stat # As above
import subprocess # Required to run external commands -> find

def check_mode(file, expected_mode):
    """
    Check the 'file' for 'expected_mode' expected permissions)
    as an octal value '0000'
    """
    full_perms = oct(os.stat(file)[0])
    mode = full_perms[-4:] 
    print_info("Mode for " + file + ": " + mode)
    print_info("    ^[" + full_perms + "]")
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

def find_global_writable():
    ROOT = "/"
    global_writable = recursive_search_permissions("/")
    print(global_writable)
    return global_writable

def recursive_search_permissions(root):
    writeable_items = []
    root_contents = os.listdir(root)
    try:
        for item in root_contents:
            writeable_perms = ['2', '3', '6', '7']
            full_perms = oct(os.stat(root+item)[0])
            kind = full_perms[:-4]
            mode = full_perms[-4:] 
            world = mode[3]
            if (world in writeable_perms):
                print_info(root + item + " is global writable [" + world + "]")
                writeable_items.append(root+item)
            """
            FOR SOME REASON If the block below exists then some files like /tmp
            are missed!!! WTF. @Future please find out what the heck is happening. It's not even that /tmp is missed its more like the
            block above doesn't even run. But then if you comment out the block
            below this, it does.
            """
            if(kind == "0o4"):
                writeable_items.extend(recursive_search_permissions(
                         root+item + "/"))
    except Exception as error:
        print_error(str(error))
    return writeable_items
    # EXPORT THIS LIST AS JSON WHEN IT WORKS

def sanity_check_globals(global_files):
    pass #@FUTURE

def sguid_search():
    pass

def main(outdir):
    set_logging(outdir + "permissions.log")
    print_title("UNIX Permission Check")
    print_subtitle("Created by Jorel Paddick\n")
    # Do a basic check of the /etc/ file permissions (inc passwd)
    check_etc()
    # Search for globally writeable files
    global_files = find_global_writable() #@FUTURE Multi-task this
    # Check if these files are not in home directories or tmp
    sanity_check_globals(global_files)
    # get a list of invalid SUID and GUID files
    sguid_search()

if __name__ == "__main__":
    main("./")