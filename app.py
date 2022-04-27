import auth
import os
import getpass
import sys

def login():
    lock = ["", " @@@@@@@ ", " @@     @@ ", " @       @ "," @       @ ","@@@@@@@@@@@","@@@@@@@@@@@","@@@@@ @@@@@","@@@@@ @@@@@","@@@@@@@@@@@","@@@@@@@@@@@", "", "passmgr", "", ""]
    os.system("clear")
    width = os.popen("stty size", 'r').read().split()[1]
    while True:
        if os.path.isfile(f"{os.getenv('HOME')}/passmgr_data/password") is True:
            login_status = True
            while True:
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                if login_status is False:
                    print("Master Password is incorrect, please try again!")
                    print("")
                print("Enter Master Password:".center(int(width)))
                password = getpass.getpass("".center(round(int(width)/2)-1))
                login_status = auth.login(password)
                del password
        else:
            # Is it the second time in the infinite loop
            password1 = None
            password2 = None
            isIt2nd = False
            while True:
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                # If it is the second time in the loop print these
                if isIt2nd is True:
                    if len(password1) < 8:
                        print("Registration failed! The password must be")
                        print("at least 8 characters long. Please Try Again!")
                        print("")
                    else:
                        print("Registration failed! The two passwords")
                        print("don't match. Please Try Again!")
                        print("")
                print("Set Master Password:")
                password1 = getpass.getpass("")
                if len(password1) < 8:
                    isIt2nd = True
                    continue
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                print("Reenter Master Password:")
                password2 = getpass.getpass("")
                # Compare if passwords are same
                if password1 == password2:
                   # Register the password
                   auth.register(password1)
                   # Reset the password variables
                   del password1
                   del password2
                   break
                else:
                    # If the passwords do not match restart the loop and print the 'Registration Failed!' text
                    isIt2nd = True
            break

def quit_app():
    os.system("clear")
    sys.exit()

