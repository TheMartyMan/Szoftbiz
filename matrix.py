import os, sys, glob, signal
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWRITE, S_IWGRP, S_IWOTH


# If the user forces a stop with Ctrl + C

def signal_handler(sig, frame):
    print("The program was interrupted by the user.")
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)


# Reading Access Control List per user

def getPerms(user):
    with open("ACL.txt", "r") as f:
        for line in f:
            if line.startswith(user + ";"):
                permissions = line.strip().split(";")[1:]
                print(f"\nHi {user}, you have the following permissions:\n{permissions}\n")
                return permissions
    print(f"User {user} does not exist.")
    exit()


# Set permissions

def setRO(file):
    os.chmod(file, S_IREAD | S_IRGRP | S_IROTH)

def setRW(file):
    os.chmod(file, S_IREAD | S_IWRITE | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH)



# Get all resources (File*.txt) from current folder

def getResources():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    pattern = os.path.join(current_dir, "File*.txt")
    return glob.glob(pattern)



# Adding a read permission to every user for the new file

def updateACLAddRead():

    with open("ACL.txt", "r") as f:
        lines = f.read().splitlines()
    new_lines = []
    for line in lines:
        if not line.endswith(";r"):
            new_lines.append(line + ";r")
        else:
            new_lines.append(line)
    with open("ACL.txt", "w") as f:
        for line in new_lines:
            f.write(line + "\n")
    print("ACL updated: Every user now has read-only permission for the new file.")

def main():
    user = input("Who are you?\n").strip()
    permissions = getPerms(user)


    newfile = input("Would you like to create a new file? [Y/N]: ").strip().lower()
    while newfile not in ['y', 'n']:
        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
        newfile = input().strip().lower()

    if newfile == 'y':
        filename = input("Please provide a file name:\n").strip()
        while not filename:
            print("Error: Filename cannot be empty!")
            filename = input("Please provide a file name:\n").strip()
        with open(filename, 'w') as new_file:
            pass
        setRO(filename)
        print(f"'{filename}' created.")
    else:
        print("Goodbye")
        exit()

    resources = getResources()
    for i, resource in enumerate(resources):
        if i < len(permissions):
            perm = permissions[i].lower()
            if perm == 'r':
                setRO(resource)
                print(f"For resource '{resource}' read only permission was set.")
            elif perm == 'rw':
                setRW(resource)
                print(f"For resource '{resource}' read and write permission was set.")
            else:
                print(f"For resource '{resource}' there were no modification regarding the permissions. (Still '{perm}').")
        else:
            print(f"There is no permission set for resource '{resource}'.")


    # Update ACL with read only for the new file
    updateACLAddRead()

if __name__ == "__main__":
    main()