import metodos

resp = None

def register():
    print("")
    print("REGISTER")
    user = input("Username: ")
    passw = input("password: ")
    ans = metodos.register(user, passw)
    if (ans):
        print("")
        print("Account created!")
        menu()
    else:
        print("")
        print("Account creation failed :(")
        exit()

def logIn():
    print("")
    print("LOG IN")
    user = input("Username: ")
    passw = input("password: ")
    clientResp = metodos.Client(user, passw, 'redes2020.xyz')

    return clientResp

def logOut(resp):
    print("")
    print("LOG OUT")
    ans = input("Do you really want to log out? (y/n): ")
    if ans == "y" or ans == "Y":
        resp.logout()
        print("")
        print("You have succesfully signed out from your account!")
    else:
        return

def deleteAccount(resp):
    print("")
    print("ERASE ACCOUNT")
    user = input("Enter the username you want to delete: ")
    resp.deleteAccount(user)
    print("Account deleted")

def addUser(resp):
    print("")
    print("ADD TO CONTACTS")
    user = input("Enter the username you want to add to your contacts: ")
    ans = resp.addUser(user)
    if ans == 1:
        print("User added to your contacts")
    else:
        return

def directMessage(resp):
    print("")
    print("SEND DIRECT MESSAGE")
    user = input("Enter the username: ")
    messg = input("Enter the message: ")
    resp.sendMessage(user, messg)
    print("")
    print("Message sent to: " + str(user))
    print(str(messg))

def joinChatRoom(resp):
    print("")
    print("JOIN CHATROOM")
    room = input("Enter the room you wanna join: ")
    roomAlias = input("Enter your alias for the room: ")

    funResp = resp.joinChatRoom(room, roomAlias)
    if (funResp):
        print("You joined the room: " + room + " as " + roomAlias)
    else:
        print("Invalid room name")
        menu()

def createChatRoom(resp):
    print("")
    print("CREATE CHATROOM")
    room = input("Enter the room you wanna create: ")
    roomAlias = input("Enter your alias for the room: ")
    resp.createChatRoom(room, roomAlias)

def roomMessage(resp):
    print("")
    print("SEND MESSAGE TO CHATROOM")
    room = input("Enter the room you wanna chat: ")
    message = input("Enter message: ")

    resp.message_room(room, message)
    print(room + ': ' + message)

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
        7. Send direct message to a contact
        8. Create a chat room
        9. Join a chat room
        10. Send a message to a joined chat room
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
        deleteAccount(resp)
    elif opt=="5":
        resp.viewContacts()
    elif opt=="6":
        addUser(resp)
    elif opt=="7":
        directMessage(resp)
    elif opt=="8":
        createChatRoom(resp)
    elif opt=="9":
        joinChatRoom(resp)
    elif opt=="10":
        roomMessage(resp)
    elif opt=="0":
        print("BYE! SEE YOU LATER :)")
        exit()
    menu()

menu()

