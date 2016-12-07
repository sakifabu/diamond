'''Author :Sakif Abu
Purpose : pysftp with hashing
	pyro4 object dameon
'''




import pysftp ,hashlib, Pyro4
from pymongo import MongoClient
#pyro4 stuff

#pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None    # disable host key checking.


cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109}
try:
  with pysftp.Connection(**cinfo) as sftp:
    try:
	payload= (open('payload.json').read()
	checksum = hashlib.md5(payload).hexdigest()
	print ('sftp used and the checksum = ',checksum)
        sftp.cd('/home/AbuSakif')               # temporarily chdir to public
        sftp.put('payload.json','/home/AbuSakif/ProjectDiamond/payload.json')
	message= {'transfertype':'Sftp used for transfer'}
	log = MongoClient().DiamondloggingSakif
	log.sftp.insert(message)
	print ('Sftp transfer done')
    except:
        print "File transfer issue"
except Exception, err:
 print err
