'''Author :Sakif Abu
Purpose : socket transfer with ssl 
	rabbit mq with AES encryption
'''
import socket, ssl
import pprint, urllib, urllib2, pika
from pymongo import MongoClient
from Crypto.Cipher import AES


title='frozen'
url = 'http://omdbapi.com/?'
param = {'t':title,'y':'','plot':'short','r':'json'}
value = urllib.urlencode(param)
response = urllib2.urlopen(url+value)
payload = response.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect(('localhost', 10022))


print repr(ssl_sock.getpeername())
print ssl_sock.cipher()
print pprint.pformat(ssl_sock.getpeercert())

ssl_sock.write(payload)

print('payload sent via socket to diamond2 ')

#This is where we listen for the return message from node 4
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='rabbitmessage')
print ' [*] Waiting for payload. To exit press CTRL+C'

#The message is parsed and decrypted
def callback(ch, method, properties, body):
        aesObj  = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        message = aesObj.decrypt(body)
       # message =body
        print(" [x] Received %r" % message)
	message1={'transfertype' : 'RabbitMQ transfer done'}
	log = MongoClient().DiamondloggingSakif
	log.rabbit.insert(message1)
	print('message received from diamond4 via rabbitmq')


channel.basic_consume(callback,
                      queue='rabbitmessage',
                      no_ack=True)


channel.start_consuming()
