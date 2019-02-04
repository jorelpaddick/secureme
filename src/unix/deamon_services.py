#!/usr/local/bin/python3
#############################################################################
# AUTHOR: Jorel Paddick 
# FILE: deamon_services.py
# CREATED: 31-01-2019
# MODIFIED: 
# PURPOSE: 
#############################################################################
import subprocess
import time
import json
import utils.termout as termout

FILENAME = "psout"
OUTPUT_NAME = "processes.json"

class Process(object):
    def __init__(self, name, pid, tty, time, cmd):
        self.name = name
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd

    def unique(self):
        return self.name

def create_dict_from_list(serial_list):
    export_dict = dict()
    for item in serial_list:
        export_dict[item.unique()] = item.__dict__
    return export_dict

def read_process_list(filename):
    processes = []
    termout.print_info("Sorting process information")
    try:
        with open(filename, 'r') as plist:
            # read the lines of the file
            lines = plist.readlines()
            # remove the first line as it is only a table descriptor
            del lines[0]
            # Iterate through all remaining lines
            name_num = 0
            for line in lines:
                fields = line.split()
                pid = fields[0]
                tty = fields[1]
                time = fields[2]
                del fields[0]
                del fields[0]
                del fields[0]
                cmd = ""
                cmd_path = fields[0]
                path_split = cmd_path.split('/')
                name = path_split.pop() 
                name += "_" + str(name_num)
                name_num += 1
                for field in fields:
                    cmd += " " + field
                process = Process(name, pid, tty, time, cmd)
                processes.append(process)
    except Exception as error:
        termout.print_error(str(error))
    return processes

def check_system(output):
    status = 0
    global FILENAME
    termout.print_info("Calling subprocess")
    filename = output + FILENAME
    try:
        with open(filename, 'w') as outfile:
            subprocess.Popen(["ps", "-A"], stdout=outfile)
            termout.print_ok("Subprocess called - File Opened")
            termout.print_info("Waiting for data...")
            time.sleep(5)
            outfile.close()
        termout.print_ok("Process data obtained")
    except Exception as error:
        termout.print_error(str(error))
        status = 1
    return status

def obtain_process_list(output):
    global FILENAME 
    proc_list = None
    termout.print_info("obtaining process list")
    if(check_system(output) == 0):
        proc_list = read_process_list(output + FILENAME)
    else:
        termout.print_error("System ps error")
    return proc_list


def export_json(json_string, filename):
    try:
        with open(filename, 'w') as f_handle:
            f_handle.write(json_string)
    except Exception as error:
        termout.print_error("Failed to write to file - " + str(error))
    

def main(outdir):
    global OUTPUT_NAME
    termout.print_title("System Process Analyser")
    termout.print_subtitle("Created by Jorel Paddick")
    termout.print_emphasis("Staring module")
    # Obtain a list of current processes
    proc_list = obtain_process_list(outdir)
    termout.print_ok(str(len(proc_list)) + " processes detected")
    # Convert this list into a dictionary
    termout.print_info("Exporting process list to file")
    proc_dict = create_dict_from_list(proc_list)
    # Convert the list into JSON
    json_data = json.dumps(proc_dict, indent=4)
    # Write the json to an output file in outdir
    try:
        export_json(json_data, outdir + OUTPUT_NAME)
        termout.print_ok("Exported")
    except Exception as error:
        termout.print_error(str(error))

if __name__ == "__main__":
    # main()
    pass