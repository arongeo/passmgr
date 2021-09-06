import crypt
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
                if password == "q" or password == "quit" or password == "exit":
                    os.system("clear")
                    quit()
                login_status = auth.login(password)
                password = "nothingtoseehere"
        else:
            # Is it the second time in the infinite loop
            isIt2nd = False;
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
                if password1 == "q" or password1 == "quit" or password1 == "exit":
                    os.system("clear")
                    quit()
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                print("Reenter Master Password:")
                password2 = getpass.getpass("")
                if password2 == "q" or password2 == "quit" or password2 == "exit":
                    os.system("clear")
                    quit()
                # Compare if passwords are same
                if password1 == password2:
                   # Register the password 
                   auth.register(password1)
                   # Reset the password variables
                   password1 = "nothingtoseehere"
                   password2 = "nothingtoseehere"
                   break
                else:
                    # If the passwords do not match restart the loop and print the 'Registration Failed!' text
                    isIt2nd = True
            break

def quit_app():
    os.system("clear")
    quit()

