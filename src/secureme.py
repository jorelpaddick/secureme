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

def get_platform():
    """Gets the current OS platform this is running on"""
    print("Checking Platform... ")
    print("Machine Type: " + platform.machine())
    print("Name (not FQDN): " + platform.node())
    print("OS: " + platform.system())
    print("Release: " + platform.release())
    print("CPU: " + platform.processor())
    print("Verbose: " + platform.platform())
    print("Version: " + platform.version())

    return platform.system()

# def load_path(path):
#     """Checks that the given path is an accessible 
#        directory and gets the contents within"""
#     if os.path.isdir(path):
#        contents = os.listdir(path) 
#     else:
#         raise IOError("cannot access directory: " + path)

#     return contents
 
# def load_unix_scripts():
#     """Targets the unix scripts directory and collates the runnable
#         scripts for exectution."""
#     print("Loading UNIX Generic Scripts...")
#     path = "scripts/unix/"

#     contents = load_path(path)

#     scripts = []

#     for item in contents:
#         if os.path.isfile(path + item):
#             item_name, item_ext = os.path.splitext(path + item)
#             if ".sh" in item_ext or ".py" in item_ext:
#                 print(item_name + " script found")
#                 scripts.append(item_name + item_ext)

#     return scripts

# def load_darwin_scripts():
#     """Targets the macos scripts directory and collates the runnable
#         scripts for exectution."""
#     print("Loading Darwin Scripts...")

#     path = "scripts/macos/"

#     contents = load_path(path)

#     scripts = []

#     for item in contents:
#         if os.path.isfile(path + item):
#             item_name, item_ext = os.path.splitext(path + item)
#             """NOTE: Could also add support for apple scripts here"""
#             if ".sh" in item_ext or ".py" in item_ext:
#                 print(item_name + " script found")
#                 scripts.append(item_name + item_ext)

#     return scripts

# def load_linux_scripts():
#     """Targets the linux scripts directory and collates the runnable
#         scripts for exectution."""
#     print("Loading Linux Scripts...")
#     path = "scripts/linux/"
#     contents = load_path(path)
#     scripts = []
#     for item in contents:
#         if os.path.isfile(path + item):
#             item_name, item_ext = os.path.splitext(path + item)
#             """NOTE: Could also add support for apple scripts here"""
#             if ".sh" in item_ext or ".py" in item_ext:
#                 print(item_name + " script found")
#                 scripts.append(item_name + item_ext)

#     return scripts

# def execute_scripts(scripts):
#     """Exectute a given list of scripts"""
#     import subprocess
#     print("\n!!!! Launching Scripts !!!!\n")
#     for script in scripts:
#         try:
#             subprocess.call(script)
#         except Exception as e:
#             print("Failed to run script: " + script)
#             print(e)

def perform_unix_checks():
    import unix.passwd_anomalies
    import unix.executable_signature

    unix.passwd_anomalies.main()
    unix.executable_signature.main()

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
    print("==== Secure Me Script for Kiddies ==== ")
    print("** Writen By Jorel Paddick **")
    
    platform = get_platform()
    time.sleep(1)
    print("Loading scripts. Press CTR-C to Stop")

    if(platform == 'Darwin'):
        perform_unix_checks()
        # scripts = load_unix_scripts() 
        # scripts.extend(load_darwin_scripts())
        time.sleep(1)
        # execute_scripts(scripts)
    elif platform == 'Linux':
        perform_unix_checks()
        # scripts = load_unix_scripts() 
        # scripts.extend(load_linux_scripts())
        time.sleep(1)
        # execute_scripts(scripts)
    elif platform == 'Windows':
        print("Windows is not yet Supported")
        time.sleep(1)
        # execute_scripts(scripts)
        print("Abort.")
    else:
        print("Operating System " + platform + " is not suppored. \nAbort. ")
        exit(-1)
            
if __name__ == '__main__':
    main()
