'''Author :Sakif Abu
Purpose : pysftp with hashing
	pyro4 object dameon
'''




import pysftp ,hashlib, Pyro4
from pymongo import MongoClient
#pyro4 stuff
import Pyro4

name = open('payload.json').read()

turnto16 = 16 - (len(name) % 16)
for i in range(turnto16):
	name += ' '
#length = len(name)%16
#name = bytes([length])*length
diamond = Pyro4.Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
print(diamond.send(name))
#pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None    # disable host key checking.


cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109}
try:
  with pysftp.Connection(**cinfo) as sftp:
    try:
	payload= open('payload.json').read()
	checksum = hashlib.md5(payload).hexdigest()
	print ('sftp used and the checksum = ',checksum)
        sftp.cd('/home/ftpuser')               # mporarily chdir to public
        sftp.put('payload.json')
	message= {'transfertype':'Sftp used for transfer'}
	log = MongoClient().DiamondloggingSakif
	log.sftp.insert(message)
	print ('Sftp transfer done')
    except:
        print "File transfer issue"
except Exception, err:
 print err
