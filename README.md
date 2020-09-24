<div align="center">
    <img src="xmpp.png" alt="xmpp" width="664"> 
  <br>
  <h2>
    Project # 2 - XMPP Protocol
  </h2>
  <h3>
    Redes 2020 
  </h3>

  <hr />

  <h3>
    Rodrigo Samayoa 
  </h3>

  <h5>
    17332 
  </h5>

  <hr />
</div>

## Description

This is the second project of the redes class at Universidad del Valle de Guatemala. Its purpose is to use the xmpp protocol to create a client that can connect to an existing server and has the basic functionality of a chat.

## Requirements

You need to have installed Python 3.8.1 `https://www.python.org/downloads/`
To see the version of python run `python --version`


#### Libraries

- threading
Installed with python
- sleekxmpp 1.3.3
`pip install sleekxmpp==1.3.3`
- xmpp 0.6.1
`pip install xmpppy==0.6.1`
- sys
Installed with python

## Files

- `client.py`
Is the main document. It has the menu and all the calls to the methods of the class Client of metodos.py
- `metodos.py`
It has all the methods that are used to show the results that the options of the menu request.


## Implemented functionalities

- Register an account
- Sign in
- Sign out
- Delete account
- View contacts
- Add a user to my contacts
- Send direct message to a contact
- Create a chat room
- Join a chat room
- Send a message to a joined chat room
- Precence message
- Notifications

## Usage
First you need to clone the repository. Run `git clone https://github.com/sam17332/redesProyecto2`.
Inside of the directory run `python3 client.py` to start the client.

#### Register an account  - Option 1
If you don't have and account, select the option 1. Then enter a username of you choice followed by the server `@redes2020.xyz`, for example `myName@redes2020.xyz` and enter a password. If you already have an account select option 2 to sign in.

#### Sign in - Option 2
If you already have an account, select the option 2 and sign in with your username `myName@redes2020.xyz` and your password. If you don't hava an accoun, select option 1.

#### Log out - Option 3
To use this option you need to be loged in. 
When you select it, it will ask you if you really want to sign out, so you have to enter "y" for yes or "n" for no.

#### Delete account - Option 4
You have to enter the account you want to delete, for example `myName@redes2020.xyz`.

#### View contacts - Option 5
To use this option you need to be loged in.
The only thing you have to do is enter 5 and it will show you the contacts of the your account.

#### Add a user to my contacts - Option 6
To use this option you need to be loged in.
To add someone to your contacts you have to enter his account, for example `myFriend@redes2020.xyz`.

#### Send direct message to a contact - Option 7
To use this option you need to be loged in.
To send a message to a contact, you have to enter the account, for example `myFriend@redes2020.xyz`, and then enter the message you wanna send.

#### Create a chat room - Option 8
To use this option you need to be loged in.
To create a chatroom you have to enter the name of the chatroom you wanna create, for example `myRoom@conference.redes2020.xyz` and then you have to enter the alias you want to have on the chatroom, for example myAlias.

#### Join a chat room - Option 9
To use this option you need to be loged in.
To join a chatroom you have to enter the name of the chatroom you wanna create, for example `myRoom@conference.redes2020.xyz` and then you have to enter the alias you want to have on the chatroom, for example myAlias.

#### Send a message to a joined chat room - Option 10
To use this option you need to be loged in and need to join a chatroom.
Once you've join a chatroom you have to enter the name of the chatroom, for example `myRoom@conference.redes2020.xyz`, and then enter the message you wanna send.

#### Exit - Option 0
If you want to kill the program select this option.

## XMPP Documentation
There's a document document named "XMPP-The definitive guide.pdf" on the repository, it has everything you need to know about XMPP.

## References
- XMPP-The definitive guide.pdf
- https://github.com/fritzy/SleekXMPP/blob/develop/examples/roster_browser.py
- https://xmpp.org
- https://slixmpp.readthedocs.io/api/stanza/iq.html