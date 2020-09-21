import time
import base64
import binascii
import threading
import sleekxmpp
import xmpp, sys
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase


def register(user, passw):
    jid = xmpp.JID(user)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()

    if xmpp.features.register(cli,jid.getDomain(),{'username':jid.getNode(),'password':passw}):
        return True
    else:
        return False

class Client(sleekxmpp.ClientXMPP):
    def __init__(self, username, password, instance_name=None):
        jid = "%s/%s" % (username, instance_name) if instance_name else username
        super(Client, self).__init__(jid, password)

        self.instance_name = instance_name
        self.username = username
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.receive)
        self.add_event_handler("changed_subscription", self.alertFriend)
        self.add_event_handler("changed_status", self.wait_for_presences)

        self.received = set()
        self.contacts = []
        self.presences_received = threading.Event()
        
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199') 
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        self.register_plugin('xep_0065')
        self.register_plugin('xep_0047', {
            'auto_accept': True
        })

        if self.connect():
            print("Login successfull")
            self.process(block=False)
        else:
            raise Exception("Unable to establish connection")

    def logout(self):
        self.disconnect(wait=False)

    def start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
        roster = self.get_roster()
        for r in roster['roster']['items'].keys():
            self.contacts.append(r)
        for jid in self.contacts:
            self.sendNotification(jid, 'Hi, im ready to chat', 'active')

    def alertFriend(self):
        self.get_roster()

    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    def sendNotification(self, to, body, ntype):
        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body
        if (ntype == 'active'):
            itemXML = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (ntype == 'composing'):
            itemXML = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (ntype == 'inactive'):
            itemXML = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")

        message.append(itemXML)
        try:
            message.send()
        except IqError as e:
            raise Exception("Unable to send active notification", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding")

    def receive(self, message):
        if len(message['body']) > 3000:
            print("You've received an image!")
            received = message['body'].encode('utf-8')
            received = base64.decodebytes(received)
            with open("imageToSave.png", "wb") as fh:
                fh.write(received)
        else:
            from_account = "%s@%s" % (message['from'].user, message['from'].domain)
            print(from_account, message['body'])

    def addUser(self, user):
        try:
            self.send_presence_subscription(pto=user)
            return 1
        except IqError:
            raise Exception("Unable to add the user to your contacts")
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding") 

    def sendMessage(self, user, message):
        self.sendNotification(user, ' Writing a message', 'composing')
        time.sleep(5)
        self.send_message(mto=user,mbody=message,mtype="chat")

