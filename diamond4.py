'''Author :Sakif Abu
Purpose : Pyro4 object broker
	 rabbit mq message sender
'''


import pika,Pyro4 ,urllib, urllib2,json
from Crypto.Cipher import AES

#pyro4



#rabbitmq
title='frozen'
url = 'http://omdbapi.com/?'
param = {'t':title,'y':'','plot':'short','r':'json'}
value = urllib.urlencode(param)
response = urllib2.urlopen(url+value)
payload = response.read()

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
