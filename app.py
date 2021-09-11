import auth
import os
import getpass

global_aes = []
global_db_key = ""

def login():
    lock = ["", " @@@@@@@ ", " @@     @@ ", " @       @ "," @       @ ","@@@@@@@@@@@","@@@@@@@@@@@","@@@@@ @@@@@","@@@@@ @@@@@","@@@@@@@@@@@","@@@@@@@@@@@", "", "passmgr", "", ""]
    os.system("clear")
    height, width = os.popen("stty size", 'r').read().split()
    while True:
        if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password") == True:
            login_status = True
            while True:
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                if login_status == False:
                    print("Master Password is incorrect, please try again!")
                    print("")
                print("Enter Master Password:")
                password = getpass.getpass("")
                login_status = auth.login(password)
                del password
        else:
            # Is it the second time in the infinite loop
            isIt2nd = False
            while True:
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                # If it is the second time in the loop print these
                if isIt2nd == True:
                    print("Registration failed! Please Try Again!")
                    print(" ")
                print("Set Master Password:")
                password1 = getpass.getpass("")
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
    quit()

