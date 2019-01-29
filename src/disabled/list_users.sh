#!/bin/bash
RESTORE=$(echo -en '\033[0m')
RED=$(echo -en '\033[00;31m')
GREEN=$(echo -en '\033[00;32m')
YELLOW=$(echo -en '\033[00;33m')
BLUE=$(echo -en '\033[00;34m')
MAGENTA=$(echo -en '\033[00;35m')
PURPLE=$(echo -en '\033[00;35m')
CYAN=$(echo -en '\033[00;36m')
LIGHTGRAY=$(echo -en '\033[00;37m')
LRED=$(echo -en '\033[01;31m')
LGREEN=$(echo -en '\033[01;32m')
LYELLOW=$(echo -en '\033[01;33m')
LBLUE=$(echo -en '\033[01;34m')
LMAGENTA=$(echo -en '\033[01;35m')
LPURPLE=$(echo -en '\033[01;35m')
LCYAN=$(echo -en '\033[01;36m')
WHITE=$(echo -en '\033[01;37m')

echo $YELLOW "*** UNIX User Account Checker ***"
echo "- Author: Jorel Paddick - "
echo $RED "Please ensure you run this as root."

echo $RESTORE

echo $CYAN "=== Obtaining Users in /etc/passwd ==="
raw_user_list=$(cat /etc/passwd | grep -v \# | cut -d : -f 1,2)
echo $RESTORE Done.

for user in $raw_user_list; do 
    echo $user
done

echo $CYAN "=== Disabled Users in /etc/passwd ==="
for user in $raw_user_list; do
    disabled_users=$(echo $user | grep ":*")
    #disabled_users="$disabled_users $(echo $user | grep ":!")"
done

if [ -z $disabled_users ] ; then
    echo $RED "None"
else
    for disabled in $disabled_users; do
        echo $RESTORE $disabled
    done
fi

echo $CYAN "=== Enabled Users in /etc/passwd ==="
for user in $raw_user_list; do
    enabled_users=$(echo $user | grep -v -E ":(\|!)")
done

if [ -z $enabled_users] ; then
    echo $RED "None"
else 
    for enabled in $enabled_users; do
        echo $RESTORE $enabled
    done
fi

echo $CYAN "=== Cheking For Mulitple Root Level Users ==="
raw_user_list=$(cat /etc/passwd)
for user in $raw_user_list; do
    roots=$(echo $user | grep ":0:")
    for root in $roots; do
        echo $RED $root
    done
done

echo $RESTORE
