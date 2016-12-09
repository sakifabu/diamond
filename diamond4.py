'''Author :Sakif Abu
Purpose : Pyro4 object broker
	 rabbit mq message sender
'''


import pika,Pyro4 ,urllib, urllib2,json
from Crypto.Cipher import AES
from pymongo import MongoClient
#pyro4


'''
#rabbitmq
title='frozen'
url = 'http://omdbapi.com/?'
param = {'t':title,'y':'','plot':'short','r':'json'}
value = urllib.urlencode(param)
response = urllib2.urlopen(url+value)
payload = response.read()'''
@Pyro4.expose
class diamond(object):
    def send(self, name):
                payload = name
		Obj  = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
		length = 16 - (len(payload)%16)
		payload +=bytes([length])*length
		message = Obj.encrypt(payload)
#message =payload
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='rabbitmessage')
		channel.basic_publish(exchange='',routing_key='rabbitmessage',body=message)
		connection.close()
		message1={'transfertype' : 'pyro has been used'}
		log = MongoClient().DiamondloggingSakif
		log.rabbit.insert(message1)

		return name
daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(diamond)   # register the greeting maker as a Pyro object
ns.register("example.greeting", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
