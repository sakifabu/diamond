'''Author :Sakif Abu
Purpose : socket transfer with ssl 
         pysftp with compression
'''


import socket, ssl, pysftp, hashlib
from pymongo import MongoClient


bindsocket = socket.socket()
bindsocket.bind(('', 10022))
bindsocket.listen(5)


run=True

#ssl receive and create file
def do_something(connstream, data):
        print "do something: ", data
	print('message received from diamond1')
        file = open('payload.json', 'w')
        file.write(data)
        file.close()
        run=False
        return False


def deal_with_client(connstream):
        data = connstream.read()
        while data:
                if not do_something(connstream, data):
                        break
                data = connstream.read()


while run:
        newsocket, fromaddr = bindsocket.accept()
        connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="server.crt", keyfile="server.key")
        try:
		message1={'transfertype' : 'Socket Transfer done'}
		log = MongoClient().DiamondloggingSakif
		log.socket.insert(message1)
                deal_with_client(connstream)
        finally:
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()

#sftp
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None    # disable host key checking.


		cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109}
		with pysftp.Connection(**cinfo) as sftp:
			payload = open('payload.json').read()
			cheksum = hashlib.md5(payload).hexdigest()	
       			sftp.cd('/home/ftpuser')               # temporarily chdir to public
       			sftp.get('alanFile.json')  # upload file to public/ on remote

