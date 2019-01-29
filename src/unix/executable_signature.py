#!/usr/local/bin/python3
import sys
import os
import utils.termout as termout
import hashlib
import json

BLOCKSIZE = 65536

def load_path(path):
    """Checks that the given path is an accessible 
       directory and gets the contents within"""
    if os.path.isdir(path):
       contents = os.listdir(path) 
    else:
        raise IOError("cannot access directory: " + path)
    return contents

def bin_analyser(path):
    global BLOCKSIZE 
    contents = load_path(path)
    termout.print_ok("Found " + str(len(contents)) + " items in " + path)
    execs = dict()
    for item in contents:
        full_path = path + item
        if os.path.isfile(full_path):
            execs[item] = hasher(full_path)
    termout.print_ok(str(len(execs))+ " hashes calculated - see logs")
    return execs

def hasher(path):
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
                return hasher.hexdigest()
    except PermissionError as perror:
        termout.print_error("Could not open file: " + str(perror) + 
                "\n    please ensure root permissions")

def jsonize(dictionary):
    return json.dumps(dictionary, indent=4)

def export_json(json_string, filename):
    try:
        with open(filename, 'w') as f_handle:
            f_handle.write(json_string)
    except Exception as error:
        termout.print_error("Failed to write to file - " + str(error))

def main():
    # Enable logging to file
    termout.set_logging("executable_signatures.log")
    termout.print_title("Simple Binary Signature Analyser")
    termout.print_subtitle("Writen by Jorel Paddick 2019")
    termout.print_emphasis("Starting module.")
    termout.print_info("Checking single user mode executables...")
    # Decalre a new dictionary to store executables
    execs = dict()
    # List single user mode binaries
    execs["/bin/"] = bin_analyser("/bin/")
    execs["/sbin/"] = bin_analyser("/sbin/")
    execs["/urs/bin/"] = bin_analyser("/usr/bin/")
    execs["/usr/local/bin/"] = bin_analyser("/usr/local/bin/")
    execs["/usr/sbin/"] = bin_analyser("/usr/sbin/")
    # Serialise the hashes
    json_formated_execs = jsonize(execs)
    export_json(json_formated_execs, "executable_signatures.json")

if __name__ == "__main__":
    main()
