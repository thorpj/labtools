#!/usr/local/bin/python
###
# Name:     labexec
# Purpose:  This is a convenience script which allows the user to execute 
#           commands/scripts, or distribute files over ssh to a list of hosts.
#           It has Curtin University's Computer department labs hard coded as
#           this was the programs intended use.
#
# Author:   Luke Healy
# License:  MIT
# Modified: 16/09/17

import sys
import os
import datetime
import hashlib

##
# For really important colours.
class bcolors:
    HEADER      = '\033[95m'
    OKBLUE      = '\033[94m'
    OKGREEN     = '\033[92m'
    WARNING     = '\033[93m'
    FAIL        = '\033[91m'
    ENDC        = '\033[0m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'

labs            = {}
specified_hosts = []
scp_mode        = False
script_mode     = False
cmd             = ""
scp_src         = ""
scp_dst         = ""

num_complete    = 0
DOMAIN          = ".cs.curtin.edu.au"
#USER            = "special"
USER            = "17086424"
TIMEOUT         = "3"

SSH_COMMAND     = "ssh -t -o BatchMode=yes -o ConnectTimeout=" + TIMEOUT + " \
-o StrictHostKeyChecking=no "
SCP_COMMAND     = "scp -r -o BatchMode=yes -o ConnectTimeout=" + TIMEOUT + " \
-o StrictHostKeyChecking=no "
time            = datetime.datetime.now().strftime("%d-%m,%H:%M:%S")
LOG_FILE        = time + "stdout.log"
ERR_FILE        = time + "stderr.log"

##
# Initialise the labs map with host names.
def init_labs():
    labs["218"]  = [
    "lab218-a01" + DOMAIN,
    "lab218-a02" + DOMAIN,
    "lab218-a03" + DOMAIN,
    "lab218-a04" + DOMAIN,
    "lab218-a05" + DOMAIN,
    "lab218-b01" + DOMAIN,
    "lab218-b02" + DOMAIN,
    "lab218-b03" + DOMAIN,
    "lab218-b04" + DOMAIN,
    "lab218-c01" + DOMAIN,
    "lab218-c02" + DOMAIN,
    "lab218-c03" + DOMAIN,
    "lab218-c04" + DOMAIN,
    "lab218-d01" + DOMAIN,
    "lab218-d02" + DOMAIN,
    "lab218-d03" + DOMAIN,
    "lab218-d04" + DOMAIN,
    "lab218-d04" + DOMAIN]

    labs["219"]  = [
    "lab219-a01" + DOMAIN,
    "lab219-a02" + DOMAIN]

    labs["220"]  = [
    "lab220-a01" + DOMAIN,
    "lab220-a02" + DOMAIN]

    labs["221"]  = [
    "lab221-a01" + DOMAIN,
    "lab221-a02" + DOMAIN]

    labs["232"]  = [
    "lab232-a01" + DOMAIN,
    "lab232-a02" + DOMAIN]

hosts_done = []
hosts_busy = []


##
# Return a string representation of a list.
def printify_list(in_list):
    return "".join([x + "\n" for x in in_list])

##
# Print the hard coded hosts.
def print_labs():
    for key in labs.keys():
        print key + ":\n" + printify_list(labs[key])
    exit(0)

##
# Prints a message in orange.
def print_info(msg):
    print bcolors.WARNING + msg + bcolors.ENDC

##
# Print a message in green.
def print_msg(msg):
    print bcolors.OKGREEN + msg + bcolors.ENDC

##
# Print an error in red.
def print_err(msg):
    print bcolors.FAIL + msg + bcolors.ENDC

##
# Called when the "-l" option is provided, parses the chosen labs
# to execute the commands on. Appends anything specfied by "-f" option.
def specify_labs(lab_csv):
    if lab_csv == "all":
        for l in labs.values():
            specified_hosts.extend(l)
    else:
        lab_list = lab_csv.split(",")

        if len(lab_list) < 1:
            print_err("Invalid argument " + lab_csv + "\n")
            print_help()
        else:
            lab_list = filter(lambda x: x.strip() in labs.keys(), lab_list)
            for l in lab_list:
                specified_hosts.extend(labs[l])

##
# Called when the "-f" option is provided. Reads a file of hosts or IP's
# to execute commands on. Appends anythin specified after "-l".
def parse_lab_file(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print_err('Invalid argument "' + filename + 
            '". No such file or directory.')
        exit(1)

    for line in f.readlines():
        specified_hosts.append(line.strip())

##
# Parse the command to be executed. Don't allow ";".
def parse_cmd(command):
    global cmd 
    if ";" in command:
        print_err('Aborting. ";" found in command, use "-s" if you need to \
            execute multiple commands.')
        exit(1) 
    cmd = command

##
# Set the scp parameters.
def parse_scp(src, dst):
    global scp_src
    global scp_dst
    global scp_mode
    scp_root_src = src
    scp_root_dst = dst
    scp_src = dst
    scp_dst = dst
    scp_mode = True


##
# Parse the command given by the user.
def parse_args(args):
    global script_mode
    if len(args) < 2:
        print_help()

    for arg in args[1:]:
        if arg == "-h" or arg == "--help":
            print_help()
        elif arg == "-L" or arg == "--list":
            print_labs()

    idx = 1
    skip_next = False

    for arg in args[1:]:
        idx += 1

        if skip_next:
            skip_next = False
        else:
            if arg == "-l" or arg == "--labs":
                skip_next = True
                specify_labs(args[idx])
            elif arg == "-p" or arg == "--push":
                parse_scp(args[idx], args[idx + 1])
                return
            else:
                print_err('Invalid option "' + arg + '"')
                print_help()

##
# "Ping" a host with ssh.
def ping(host):
    for c in ";:,<>?/\\#$%^&*()":
        host.replace(c, "")
    return os.system(SSH_COMMAND + USER + "@" + host + " exit &> /dev/null")

##
# "Pings" all specified hosts and removes unresponsive ones from the list.
# Notify user of down hosts.
def get_num_hosts_down():
    global specified_hosts

    down_hosts = []
    up_hosts = []
    for h in specified_hosts:
        if ping(h) == 0:
            up_hosts.append(h)
        else:
            down_hosts.append(h)

    specified_hosts = up_hosts

    for d in down_hosts:
        print_info(d + " down.")

    return len(down_hosts)


##
# Prints the usage/help message.
def print_help():
    print bcolors.BOLD + "Usage: labaxec.py [-hL] [-lf targets] [-c command]"
    print "                         [-s script] [-p src dst]" + bcolors.ENDC
    print "Options:"
    print "  -h,    --help: Print this message and exit."
    print "  -L,    --list: List all labs and their hosts and exit."

    print "  -l,    --labs: Specify which lab(s) to remotely execute commands."
    print "                 (Comma separated values. E.g. 218,221,232)"
    print "\nPlease be aware that without key auth, this is basically useless."

    exit(1)

##
#
def print_progress_bar(num, total):
    total_len = 50
    progress = int(total_len * (float(num) / float(total)))
    sys.stdout.write("\r" + (progress) * u"\u2588" + int(total_len - progress) * u"\u2591" + " - " + str((float(num) * 100.0) / float(total)) + "% Complete")
    sys.stdout.flush()
    if total == num:
        print "."
##
# Execute a command over ssh.
def execute(command, host):
    print SSH_COMMAND + USER + "@" + host + " " + command + \
        " 1>> " + LOG_FILE + " 2>> " + ERR_FILE
    ret = os.system(SSH_COMMAND + USER + "@" + host + " " + command + \
        " 1>> " + LOG_FILE + " 2>> " + ERR_FILE)

    return ret

def get_host():
    for h in hosts_done:
        if h not in hosts_busy:
            return h

##
# Execute scp for a given file.
def scp(src, dst, dst_host):
    src_host = get_host()
    hosts_busy.append(src_host)
    ret = execute(SCP_COMMAND + " " + USER + "@" + src_host + ":" + src + " .", dst_host)
    hosts_busy.remove(src_host)

    return ret

##
# Calls execute on all specified hosts.
def execute_cmd():
    global specified_hosts
    global num_complete
    num_ok = 0

    for h in specified_hosts:
        if execute(cmd, h) == 0:
            num_ok += 1
            num_complete += 1
        print_progress_bar(num_complete, len(specified_hosts))
    return num_ok

##
# Calls scp on all specified hosts.
def execute_scp():
    global specified_hosts
    global num_complete
    num_ok = 0

    for h in specified_hosts:
        hosts_busy.append(h)
        if scp(scp_src, scp_dst, h) == 0:
            num_ok += 1
            num_complete += 1
            hosts_busy.remove(h)
            hosts_done.append(h)

    return num_ok

##
# Checks to see if the user wants to proceed.
def check_proceed():
    cont = raw_input("Proceed with the " + str(len(specified_hosts)) + \
        " live hosts anyway? (y/N): ")
    return (cont == "y" or cont == "Y" or cont == "yes" or cont == "YES")

##
# Wrapper to initiate the batch execution.
def exec_remote():
    if scp_mode:
        print_msg('"' + scp_src + '" successfuly pushed to ' + \
            str(execute_scp()) + " hosts.")

    print "See " + LOG_FILE + " for the output of each."

##
# Drives the execution.
def main():
    if USER == "":
        print_err("Please set the USER in labexec.py")
        exit(1)

    init_labs()
    parse_args(sys.argv)

    if len(specified_hosts) < 1:
        print_err('No hosts specified, aborting.')
        exit(1)

    else:
        if scp_mode:
            print 'Pushing "' + scp_src + '" to ' + str(len(specified_hosts)) +\
            " hosts."

    if get_num_hosts_down() > 0:
        if check_proceed():
            exec_remote()
        else:
            print_err("Command abandoned by user.")
    else:
        exec_remote()

##
# Main
if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print_err("Invalid Argument.")
        print_help()


