#!/usr/local/bin/python3
#############################################################################
# AUTHOR: Jorel Paddick (18847897)
# FILE: secureme.py
# CREATED: 21-08-2018
# MODIFIED: Thu 23 Aug 08:52:08 2018
# PURPOSE: Entry point for the secureme program
#############################################################################
""" Requried Modules """
import os # Userd to dertermine which OS is running this script
import sys # How do I even program?
import time # Used for sleeping the process
import platform # Quick and easy system analysis
import argparse # To parse command line arguments
import json # For handling JSON serialisation formations of output

class Color():
    """For printing color to the screen"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_platform():
    """Gets the current OS platform this is running on"""
    print(Color.BOLD + "Checking Platform... " + Color.END)
    print("Machine Type: " + Color.OKGREEN + platform.machine() + Color.END)
    print("Name (not FQDN): " + Color.OKGREEN + platform.node() + Color.END)
    print("OS: " + Color.OKGREEN + platform.system() + Color.END)
    print("Release: " + Color.OKGREEN + platform.release() + Color.END)
    print("CPU: " + Color.OKGREEN + platform.processor() + Color.END)
    print("Verbose: " + Color.OKGREEN + platform.platform() + Color.END)
    print("Version: " + Color.OKGREEN + platform.version() + Color.END)

    return platform.system()

def load_path(path):
    """Checks that the given path is an accessible 
       directory and gets the contents within"""
    if os.path.isdir(path):
       contents = os.listdir(path) 
    else:
        raise IOError("cannot access directory: " + path)

    return contents
 
def load_unix_scripts():
    """Targets the unix scripts directory and collates the runnable
        scripts for exectution."""
    print(Color.OKBLUE + "Loading UNIX Generic Scripts...")
    path = "scripts/unix/"

    contents = load_path(path)

    scripts = []

    for item in contents:
        if os.path.isfile(path + item):
            item_name, item_ext = os.path.splitext(path + item)
            if ".sh" in item_ext or ".py" in item_ext:
                print(Color.WARN + item_name + " script found" + Color.END)
                scripts.append(item_name + item_ext)

    return scripts

def load_darwin_scripts():
    """Targets the macos scripts directory and collates the runnable
        scripts for exectution."""
    print(Color.OKBLUE + "Loading Darwin Scripts...")

    path = "scripts/macos/"

    contents = load_path(path)

    scripts = []

    for item in contents:
        if os.path.isfile(path + item):
            item_name, item_ext = os.path.splitext(path + item)
            """NOTE: Could also add support for apple scripts here"""
            if ".sh" in item_ext or ".py" in item_ext:
                print(Color.WARN + item_name + " script found" + Color.END)
                scripts.append(item_name + item_ext)

    return scripts

def load_linux_scripts():
    """Targets the linux scripts directory and collates the runnable
        scripts for exectution."""
    print(Color.OKBLUE + "Loading Linux Scripts...")

    path = "scripts/linux/"

    contents = load_path(path)

    scripts = []

    for item in contents:
        if os.path.isfile(path + item):
            item_name, item_ext = os.path.splitext(path + item)
            """NOTE: Could also add support for apple scripts here"""
            if ".sh" in item_ext or ".py" in item_ext:
                print(Color.WARN + item_name + " script found" + Color.END)
                scripts.append(item_name + item_ext)

    return scripts

def execute_scripts(scripts):
    """Exectute a given list of scripts"""
    import subprocess
    print(Color.HEADER + "\n!!!! Launching Scripts !!!!\n")
    for script in scripts:
        try:
            subprocess.call(script)
        except Exception as e:
            print("Failed to run script: " + script)
            print(e)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', 
            help='Run with a basic interactive user interface',
            action='store_true')
    args = parser.parse_args()
    if(args.interactive == True):
        print("Hello World")
        exit(9)

    print(Color.HEADER + "==== Secure Me Script for Kiddies ==== " 
            + Color.END)
    print(Color.UNDERLINE + "** Writen By Jorel Paddick **" + Color.END)
    
    platform = get_platform()
    time.sleep(1)
    print("Loading scripts. Press CTR-C to Stop")

    if(platform == 'Darwin'):
        scripts = load_unix_scripts() 
        scripts.extend(load_darwin_scripts())
        time.sleep(1)
        
        execute_scripts(scripts)
    elif platform == 'Linux':
        scripts = load_unix_scripts() 
        scripts.extend(load_linux_scripts())
        time.sleep(1)
        execute_scripts(scripts)
    elif platform == 'Windows':
        print(Color.WARN + "Windows is not yet Supported")
        time.sleep(1)
        execute_scripts(scripts)
        print("Abort." + Color.END)
    else:
        print(Color.FAIL + "Operating System " + platform + 
            " is not suppored. \nAbort. " + Color.END)
        exit(-1)
            
    
if __name__ == '__main__':
    main()
