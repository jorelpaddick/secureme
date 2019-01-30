#!/usr/local/bin/python3
#############################################################################
# AUTHOR: Jorel Paddick (18847897)
# FILE: secureme.py
# CREATED: 21-08-2018
# MODIFIED: Thu 23 Aug 08:52:08 2018
# PURPOSE: 
#############################################################################
def set_logging(file):
    set_logging.logfile = open(file, 'w')

def kill_logging():
    set_logging.logfile.close()

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

def print_title(data):
    print(Color.HEADER+ "*** " + data + " ***" + Color.END + "\n")
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write("*** " + data + " ***\n\n")
    except AttributeError:
        pass


def print_subtitle(data):
    print(Color.UNDERLINE+ data + Color.END)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write(data + "\n")
    except AttributeError:
        pass

def print_emphasis(data):
    print(Color.BOLD + data + Color.END)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write(data + "\n")
    except AttributeError:
        pass
    
def print_info(data):
    print(Color.OKBLUE + "[INFO] " + Color.END + data)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write("[INFO] " + data + "\n")
    except AttributeError:
        pass

def print_ok(data):
    print(Color.OKGREEN + "[OK] " + Color.END + data)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write("[OK] " + data + "\n")
    except AttributeError:
        pass

def print_warning(data):
    print(Color.WARN + "[WARN] " + Color.END + data)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write("[WARN] " + data + "\n")
    except AttributeError:
        pass


def print_critical(data):
    print(Color.FAIL+ "[CRITICAL] " + data + Color.END)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write("[CRITICAL] " + data + "\n")
    except AttributeError:
        pass

def print_error(data):
    print(Color.FAIL+ "[ERROR] " + Color.END + data)
    try:
        if set_logging.logfile is not None:
            set_logging.logfile.write("[ERROR] " + data + "\n")
    except AttributeError:
        pass

# def main():
#     print("This module makes terminal logging neat.\n")
#     print(" ## Testing Colors! ## ")
#     print_title("This is a title header!")
#     print_subtitle("Subtitle headings work too!\n")
#     print_emphasis("Emphasise your points!\n")
#     print_info("This is some information!\n")
#     print_ok("This thing worked!\n")
#     print_warning("I don't know if I can code anymore\n")
#     print_error("yeah nah.\n")

# if __name__ == '__main__':
#     main()


