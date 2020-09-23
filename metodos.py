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
		self.send_presence(pshow='chat', pstatus='Available')
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
			raise Exception("Server Error")

	def sendNotificationChatRoom(self, to, body):
		message = self.Message()
		message['to'] = to
		message['type'] = 'groupchat'
		message['body'] = body

		itemXML = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")

		message.append(itemXML)
		try:
			message.send()
		except IqError as e:
			raise Exception("Unable to send active notification", e)
			sys.exit(1)
		except IqTimeout:
			raise Exception("Server Error")

	def receive(self, message):
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
			raise Exception("Server Error") 

	def sendMessage(self, user, message):
		self.sendNotification(user, ' is writing a message', 'composing')
		self.send_message(mto=user,mbody=message,mtype="chat")

	def message_room(self, room, message):
		self.send_message(mto=room, mbody=message, mtype='groupchat')

	def deleteAccount(self, account):
		delete = self.Iq()
		delete['from'] = account
		delete['type'] = 'set'
		itemXML = ET.fromstring("<query xmlns='jabber:iq:register'>\
									<remove/>\
								</query>")
		delete.append(itemXML)
		try:
			delete.send(now=True)
			print("Account deleted succesfuly")
		except IqError as e:
			raise Exception("Unable to delete account", e)
			sys.exit(1)
		except IqTimeout:
			raise Exception("Server Error") 

	# https://github.com/fritzy/SleekXMPP/blob/develop/examples/roster_browser.py
	def viewContacts(self):
		try:
			self.get_roster()
		except IqError as err:
			print('Error: %s' % err.iq['error']['condition'])
		except IqTimeout:
			print('Server Error')

		groups = self.client_roster.groups()
		for group in groups:
			print('\n%s' % group)
			print('-' * 50)
			for jid in groups[group]:
				sub = self.client_roster[jid]['subscription']
				name = self.client_roster[jid]['name']
				if self.client_roster[jid]['name']:
					print(' %s (%s) [%s]' % (name, jid, sub))
				else:
					print(' %s [%s]' % (jid, sub))

				connections = self.client_roster.presence(jid)
				for res, pres in connections.items():
					show = 'available'
					if pres['status']:
						print('       %s' % pres['status'])
		print('-' * 50)

	def joinChatRoom(self, room, roomAlias):
		try:
			self.plugin['xep_0045'].joinMUC(room, roomAlias)
			self.sendNotificationChatRoom(room, roomAlias + ' just entered the chatroom!')
			return True
		except IqError as e:
			raise Exception("Unable to create room", e)
		except IqTimeout:
			raise Exception("Server Error")

	def createChatRoom(self, room, roomAlias):
		self.plugin['xep_0045'].joinMUC(room, roomAlias, pstatus="ROOM", pfrom=self.boundjid.full, wait=True)
		self.plugin['xep_0045'].setAffiliation(room, self.boundjid.full, affiliation='owner')
		self.plugin['xep_0045'].configureRoom(room, ifrom=self.boundjid.full)
