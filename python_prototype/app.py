import getch
import crypt
import auth
import os

class App:
    def menu():
        lock = ["", " @@@@@@@ ", " @@     @@ ", " @       @ "," @       @ ","@@@@@@@@@@@","@@@@@@@@@@@","@@@@@ @@@@@","@@@@@ @@@@@","@@@@@@@@@@@","@@@@@@@@@@@", "", "passmgr", "", ""]
        os.system("clear")
        height, width = os.popen("stty size", 'r').read().split()
        if os.path.isfile("~/passmgr/password.passmgr") == True:
            print("Enter Password:")
            password = input("")
        else:
            isIt2nd = False;
            while True:
                os.system("clear")
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                if isIt2nd == True:
                    print("Registration failed! Please Try Again!")
                    print(" ")
                print("Set Password:")
                password1 = input("")
                os.system("clear")
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                print("Reenter Password:")
                password2 = input("")
                if password1 == password2:
                   auth.register(password1)
                   password1 = "nothingtoseehere"
                   password2 = "nothingtoseehere"
                   break
                else:
                    isIt2nd = True
            

App.menu()
