import metodos
from PyInquirer import prompt, print_json, Separator

resp = None

def register():
    user = input("Username: ")
    passw = input("password: ")
    ans = metodos.register(user, passw)
    if (ans):
        print("")
        print("Account created")
        menu()
    else:
        print("")
        print("Account creation failed :(")
        exit()

def logIn():
    print("LOG IN")
    user = input("Username: ")
    passw = input("password: ")
    clientResp = metodos.Client(user, passw, 'redes2020.xyz')
    return clientResp

def logOut(resp):
    print("LOG OUT")
    ans = input("Do you really want to sign out? \n (y/n): ")
    if ans == "y" or ans == "Y":
        resp.logout()
        print("")
        print("You have succesfully signed out from your account!")
    else:
        return

def addUser(resp):
    print("ADD TO CONTACTS")
    user = input("Enter the username you want to add to your contacts: ")
    ans = resp.addUser(user)
    if ans == 1:
        print("User added to your contacts")
    else:
        return

def directMessage(resp):
    print("SEND DIRECT MESSAGE")
    user = input("Enter the username: ")
    messg = input("Enter the message: ")
    resp.sendMessage(user, messg)
    print(str(user) + ": " + str(messg))

def menu():
    print(""" 
        ----------------
        | MENU OPTIONS |
        ----------------

        1. Register a new account
        2. Login
        3. Logout
        4. Delete account
        5. View contacts
        6. Add a user to my contacts
        7. View details of a contact
        8. Send direct message to a contact
        9. Join a chat room
        10. Define presence message
        11. Send notification
        12. Send files
        0. Exit
        """)

    opt = input("Select one option: ")

    if opt=="1":
        register()
    elif opt=="2":
        global resp
        resp = logIn()
    elif opt=="3":
        logOut(resp)
    elif opt=="4":
        delete()
    elif opt=="5":
        viewContacts()
    elif opt=="6":
        addUser(resp)
    elif opt=="7":
        viewDetails()
    elif opt=="8":
        directMessage(resp)
    elif opt=="9":
        chatRoom()
    elif opt=="10":
        defineMessage()
    elif opt=="11":
        sendNoti()
    elif opt=="12":
        sendFiles()
    elif opt=="0":
        print("SEE YOU LATER!")
        exit()
    menu()

menu()

