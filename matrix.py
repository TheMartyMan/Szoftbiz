import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWRITE, S_IWGRP, S_IWOTH


def getPermission(user):
    found = False
    with open("ACL.txt", "r") as f:
        acl = f.readlines()
        for line in acl:
            if user in line:
                if not found:
                    print(f"\nHi {user}, you have the following permissions:\n")
                    found = True
                    currentPerms = (line.replace(f"{user};", "").strip(";") + "\n\n").split(";")
                print(line.replace(f"{user};", "").strip() + "\n\n")
    print(currentPerms)
    if not found:
        print(f"User {user} does not exist.")
        exit()


def setReadOnly(file):
    os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)

def setWriteOnly(file):
    os.chmod(file, S_IWRITE|S_IWGRP|S_IWOTH)

def getACL():
    f=open("ACL.txt", "r")
    print("ACL:\n\n" + f.read())


def getAllUsers():
    with open("users.txt", "r") as users:
        lines = [line.rstrip() for line in users]
    users.close()
    return lines


def getUser(specificuser):
    with open('users.txt', "r") as users:
        if specificuser in users.read():
            users.close()
            return specificuser
        else:
            print("User '" + specificuser + "' not found in the users list.")
            users.close()
            return False


def getAllResources():
    with open("resources.txt", "r") as resources:
        lines = [line.rstrip() for line in resources]
    resources.close()
    return lines


if __name__=="__main__":
    user = input("Who are you?\n")
    getPermission(user)
    newfile = input("Would you like to create a new file? [Y/N]: ").strip().lower()
    while newfile not in ['y', 'n']:
        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
        newfile = input().strip().lower()

    if newfile == 'y':
        filename = input("Please provide a file name:\n")
        with open(filename, 'w') as new_file:
            new_file.close()
        with open("ACL.txt") as ACL_list:
            lines = ACL_list.read().splitlines()
        with open("ACL.txt", "w") as ACL_list:
            for line in lines:
                print(line + ";r", file=ACL_list)

    else:
        print("Goodbye!")
        exit()
