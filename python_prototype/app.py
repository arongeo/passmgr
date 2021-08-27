import getch
import crypt
import auth
import os
import curses
import getpass

global_aes_key = ""

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
                    print("Password is incorrect, please try again!")
                    print("")
                print("Enter Password:")
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
                print("Set Password:")
                password1 = getpass.getpass("")
                if password1 == "q" or password1 == "quit" or password1 == "exit":
                    os.system("clear")
                    quit()
                os.system("clear")
                # Print Lock Icon
                for i in range(len(lock)):
                    print(lock[i].center(int(width)))
                print("Reenter Password:")
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

menu_options = ['Get Password', 'Add Password', 'Quit']

def print_menu(stdscr, selected_row_index):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for index, row in enumerate(menu_options):
            x = w//2 - len(row)//2
            y = h//2 - len(menu_options)//2 + index
            if index == selected_row_index:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

    stdscr.refresh()


def curses_main_menu_config(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_index = 0
    global global_aes_key
    aes_key = global_aes_key
    global_aes_key = "nothingtoseehere"

    print_menu(stdscr, current_row_index)

    while True:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_index > 0:
            current_row_index -= 1
        elif key == curses.KEY_DOWN and current_row_index < len(menu_options)-1:
            current_row_index += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()

            if current_row_index == 0:
                stdscr.addstr(0, 0, "Passwords Will Be Here!")
            elif current_row_index == 1:
                stdscr.addstr(0, 0, "Adding Passwords Will Be Here!")
            elif current_row_index == 2:
                quit_app()
            
            current_row_index = 0
            stdscr.refresh()
            stdscr.getch()
 
        print_menu(stdscr, current_row_index)
        stdscr.refresh()

def menu(aes_key):
    global global_aes_key
    global_aes_key = aes_key
    curses.wrapper(curses_main_menu_config)

