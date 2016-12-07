from Crypto.Cipher import AES
obj =AES.new ('',AES.MODE_CBC,'')
message = input("bla bla")
ciphertext=obj.encrypt(message)
print(ciphertext)
obj2 =AES.new ('',AES.MODE_CBC,'')
print(obj2.decrypt(ciphertext))

