import getch
import crypt
import auth
import os

class App:
    def menu():
        os.system("clear")
        height, width = os.popen("stty size", 'r').read().split()
        if os.path.isfile("~/passmgr/password.passmgr") == True:
            while True:
                choice = getch.getch()
                if choice == "L" or choice == "l":
                    passmgr.auth.login()
                    break
        else:
            a = ["", " @@@@@@@ ", " @@     @@ ", " @       @ "," @       @ ","@@@@@@@@@@@","@@@@@@@@@@@","@@@@@ @@@@@","@@@@@ @@@@@","@@@@@@@@@@@","@@@@@@@@@@@", "", "passmgr"]
            for i in range(len(a)):
                print(a[i].center(int(width)))


App.menu()
