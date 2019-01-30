#!/usr/local/bin/python3
# Define the color class
import sys # for below
import utils.termout as termout
import json # import the json library
import datetime # used to get human readable time format

"""
The UNIX passwd file (/etc/passwd) tells us a great deal information
about the users on the system. This information includes:
    - username
    - password or *
    - user identifier (UID) 
    - group identifier (GID) (primary group)
    - GECOS or comment field (sometimes full name or data)
    - home directory
    - shell
This module will open the password file in a read-only manner and assess the
integrity of the file contents. The information obtained is serialised 
for further analysis. 🦊
"""

class UnixUser(object):
    def __init__(self, username, passwd, uid, gid, gecos, home, shell):
        self.username = username
        self.password = passwd
        self.uid = uid
        self.gid = gid
        self.gecos = gecos
        self.home = home
        self.shell = shell

    def serialise(self):
        return json.dumps(self.__dict__)

def user_from_passwd_line(line):
    """
    imports a line from /etc/passwd file and creates a user
    object with the receieved information
    """
    # if the line starts with a '#' then return None or Null
    if(line[0] == '#'):
        user = None
    else:
        # tokenise the line by ':'
        tokens = line.split(':')
        #The structure of passwd is defined in th block comment above.
        #Using the ':' delimeter we shall read each field into a user obect
        username = tokens[0]
        password = tokens[1]
        uid = tokens[2]
        gid = tokens[3]
        gecos = tokens[4]
        home = tokens[5]
        shell = tokens[6]
        user = UnixUser(username, password, uid, gid, gecos, home, shell)
        return user

def find_disabled_users(users):
    # create a new empty list of disabled users
    disabled_users = []
    # Check every user in the list to see if they have a disabled account
    for user in users:
        # if the password field is '*' then the user is disabled
        if user.password == '*':
            disabled_users.append(user)
    return disabled_users

def find_locked_users(users):
    # create a new empty list for locked users
    locked_users = []
    for user in users:
        if user.password[0] == '!':
            locked_users.append(user)
    return locked_users

def user_counter(users):
    disabled_users = find_disabled_users(users)
    locked_users = find_locked_users(users)
    num_users = str(len(users))
    num_disabled_users = str(len(disabled_users))
    num_locked_users = str(len(locked_users))
    termout.print_ok("Found " + num_users + " users.")
    termout.print_info(num_disabled_users + "/" + num_users + " users disabled")
    termout.print_info(num_locked_users + " locked users")


def duplicate_username_check(users_list):
    """
    Checks for duplicate user names within a list of users and 
    if there is a match the matching user will be returned.
    """
    try:
        # declare a dictionary of usernames 
        # as each user is added, set its instance count to 1
        # if the name is matched a in the table then a duplicate exists
        user_dict = dict() 
        duplicate_list = [] # return a list of duplicates
        for user in users_list:
            try:
                if(user_dict[user.username] > 0):
                    # if this line is reached then the user already has
                    # exists in the table.
                    # add it to the duplicate list
                    duplicate_list.append(user)
            # if this line is met, the user is not in the table
            except KeyError: 
                # add the user to the table and set it's instance count to 1
                user_dict[user.username] = 1
        return duplicate_list
    except Exception as error:
        termout.print_error(error)

def duplicate_uid_check(users_list):
    """
    Checks for duplicate uid numbers within a list of users and 
    if there is a match the matching user will be returned.
    """
    try:
        # declare a dictionary of usernames 
        # as each user is added, set its instance count to 1
        # if the name is matched a in the table then a duplicate exists
        user_dict = dict() 
        duplicate_list = [] # return a list of duplicates
        for user in users_list:
            try:
                if(user_dict[user.uid] > 0):
                    # if this line is reached then the user already has
                    # exists in the table.
                    # add it to the duplicate list
                    duplicate_list.append(user)
            # if this line is met, the user is not in the table
            except KeyError: 
                # add the user to the table and set it's instance count to 1
                user_dict[user.uid] = 1
        return duplicate_list
    except Exception as error:
        termout.print_error(error)

def duplicate_gid_check(users_list):
    """
    Checks for duplicate gid numbers within a list of users and 
    if there is a match the matching user will be returned.
    """
    try:
        # declare a dictionary of usernames 
        # as each user is added, set its instance count to 1
        # if the gid is matched a in the table then a duplicate exists
        user_dict = dict() 
        duplicate_list = [] # return a list of duplicates
        for user in users_list:
            try:
                if(user_dict[user.gid] > 0):
                    # if this line is reached then the user already has
                    # exists in the table.
                    # add it to the duplicate list
                    duplicate_list.append(user)
            # if this line is met, the user is not in the table
            except KeyError: 
                # add the user to the table and set it's instance count to 1
                user_dict[user.gid] = 1
        return duplicate_list
    except Exception as error:
        termout.print_error(error)

def duplication_tests(users_list):
    # check for duplicate usernames
    duplicates = []
    duplicates = duplicate_username_check(users_list)
    if(len(duplicates) > 0):
        for user in duplicates:
            termout.print_warning("Found Duplicate Username: " + user.username)
            if(user.username == "root"):
                termout.print_critical("ROOT USER DUPLICATE DETECTED")
    else:
        termout.print_ok("No duplicate usernames")
    duplicates.clear()
    duplicates = duplicate_uid_check(users_list)
    if(len(duplicates) > 0):
        for user in duplicates:
            termout.print_warning("Found Duplicate UID: " + user.uid)
            if(int(user.uid) == 0):
                termout.print_critical("ROOT USER DUPLICATE DETECTED")
    duplicates.clear()
    duplicates = duplicate_gid_check(users_list)
    if(len(duplicates) > 0):
        for user in duplicates:
            if(int(user.gid) == 0):
                termout.print_warning("Found Duplicate GID: " + user.gid + 
                    " for user " + user.username + "(" + user.uid +")")
                termout.print_critical("ROOT USER DUPLICATE DETECTED")
            else:
                termout.print_info("Found Duplicate GID: " + user.gid + 
                    " for user " + user.username + "(" + user.uid +")")
    else:
        termout.print_ok("No duplicate UIDs")

def invalid_password_check(user_list):
    """
    Check a list of users password hashes. If a hash is discovered
    it means that hash is visible in /etc/password and poses a threat.
    This function will return a list of users with erronous password 
    setups
    """
    invalid_users = []
    for user in user_list:
        if(user.password != "x" and user.password != "*" 
                and user.password != "!"):
            invalid_users.append(user)
    return invalid_users

def main(outdir):
    termout.set_logging(outdir + "passwd.log")
    termout.print_title("UNIX passwd Security Check")
    termout.print_subtitle("Created by Jorel Paddick\n")
    termout.print_info("Start: " + str(datetime.datetime.now()))
    termout.print_info("Opening passwd file")
    try:
        with open('/etc/passwd', 'r') as passwd:
            termout.print_ok("passwd open")
            termout.print_info("searching users")
            # declare an empty list of users
            users = []
            for line in passwd.readlines():
                # add each user found to the list of users if not None
                user = user_from_passwd_line(line)
                if user is not None:
                    users.append(user)
            user_counter(users)
            #pass to duplication tests
            termout.print_info("Checking duplicate fields")
            duplication_tests(users)
            termout.print_info("Checking for invalid password setups")
            # check for broken passwords
            bad_passes = invalid_password_check(users)
            if len(bad_passes) > 0:
                for bad_user in bad_passes:
                    termout.print_warning("password discovered for user: " 
                            + bad_user.username + "(" + bad_user.uid + ")" + " - " + bad_user.password)
            else:
                termout.print_ok("Password setup is correct")
            termout.print_ok("Check Completed.")
    except Exception as error:
        termout.print_error(str(error))
        termout.print_info("Exiting.")
    finally:
        termout.kill_logging()

if __name__ == "__main__":
    print("Fix Me")