#!/usr/bin/python3

# INET4031
# Luke Nelson
# 3/22/2026
# 3/22/2026

#os is used to execute system level commands, re is used for pattern matching, sys is used to read input from user
import os
import re
import sys


def main():
    dry_run = input("Run in dry mode? (Y/N): ")
    dry_run = dry_run.upper()

    for line in sys.stdin:

        match = re.match("^#",line)

        #removes white space and uses : as a delimiter to split the line into fields. 
        fields = line.strip().split(':')

        #The if statement is checking if the input has exactly 5 fields. If there is not exactly 5 fields the data is not processed
        if match or len(fields) != 5:
           if dry_run == "Y":
              print("Dry run error: Invalid line skipped:", line.strip())
           continue

        #Looks at the username and password and full name info and formats it to match the passwd file 
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        #Splits group into a list. This is for the case that a user belongs to multiple groups. 
        groups = fields[4].split(',')

        #Displays a message that says a user account is being created.
        print("==> Creating account for %s..." % (username))
        #This command creats a new user account with specified Gecos info without needing a password. 
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        if dry_run == "Y":
           print("Dry run: Would execute:", cmd)
        else:
           os.system(cmd)

        #Displays message that says a password is being set for the new user.
        print("==> Setting the password for %s..." % (username))
        #Builds a command that sets the users password by piping password into passwd command.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        if dry_run == "Y":
           print("Dry run: Would execute:", cmd)
        else:
           os.system(cmd)

        for group in groups:
            #The if statement is checking if the user should be added to a group. If the group is not  '_' the user will be added to that group.
            if group != '-':
              if dry_run == "Y":
                print("Dry run: Would assign %s to group %s" % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print("Dry run: Would execute:", cmd)
              else:
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                os.system(cmd)
            else:
             if dry_run == "Y":
                print("Dry run: Skipping group assignment for %s" % (username))

if __name__ == '__main__':
    main()
