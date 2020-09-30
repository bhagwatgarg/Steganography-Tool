import numpy as np
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from steganography import encrypt, decrypt

def keygen(password):
  salt=b'zZXU6Q5MW7hHEl66WzdQGP5xxhd2bBsr0DnFUus31GGo2gAn4ht4biztgXsquLPl4OB6TUeb2z7PUtiIvKY162wMT7xWXdzMjeS4ThaIcCxtMebctJWjYkklFr3NjJ85XsPb1yYljlBFeDq4BiTc0AIpr4LsrGptLrTZKw5gZnemFdtFuJHzV4LqI8Yc5F7pWD0Q5L7z6k1T4oLo2Pyq8i07vwPHpgDCnmOBeExcS0lpKvB4C1hXhOG8fV7UaVkr9qIi7vaFcqWBn9y6v9jwAatPLbDWcWIJotoD3CQS9zMP4g8k6zn1syF6DYRz2ia9hN3Z26y8kUMfbrqfnpZKEEkXVbNZJUnUCX7NDepabibEKLoV9pE0PYqqv9qBs0XB2vBdRmYT5ohzgdecLZor5KpCpQRrw7MjVzhac923J3rBcfb5BEAd1JBLi14dVAZkTez7nVbSJIAdFbuqakVdHlaeob7EQZkZIWysEhR7cPhcTLqCEE1FGu2oOYb9Tdh94GYX2J1wos8ZWcfCKbP7FsggZLfkdmaGvSMTsaQjILowUgB36jG90qfK4yGmo7wlyS3mhyGH2JERRRALo58YllgSh3PUKJp60WyVouLaQIckQwoe1vhGIjlqyuPyWBsDg1w13E2MIYXH0M6i2C7NEURrQHo1knLOmZl6EhaCEGhGyfcjhLo6I082VjOAukkPm0ciN3UNbbakrPBSD17KIEWJ5anKNluwwB7FxjtUmhlKjK3bxyUgOkx459TRanikiTTr5guWDsYs'
  return PBKDF2(password, salt, 96, 65000).hex()

def encryption(img_file, secret_file, password):
  msg=open(secret_file).read()
  img=plt.imread(img_file)
  if img_file[-4:]=='.png':
    img=(img*255).astype(int)
    img=img[:,:,:3]
  key= keygen(password)
  enc=AES.new(key[:32], AES.MODE_CBC, key[-16:]).encrypt(padding(msg)).hex()
  hash=SHA256.new(bytes.fromhex(enc)).hexdigest()
  token=AES.new(key[32:64], AES.MODE_CBC, key[-32:-16]).encrypt(bytes.fromhex(hash)).hex()     #length=64 (in hash)
  # print(AES.new(key[32:64], AES.MODE_CBC, key[-32:-16]).decrypt(bytes.fromhex(token)).hex())
  return encrypt(img, token+enc)

def decryption(img_file, password):
  img=plt.imread(img_file)
  if img_file[-4:]=='.png':
    img=(img*255).astype(int)
    img=img[:,:,:3]
  text=decrypt(img)
  key=keygen(password)
  decoded=AES.new(key[:32], AES.MODE_CBC, key[-16:]).decrypt(bytes.fromhex(text[64:])).decode("utf-8")
  hash1=AES.new(key[32:64], AES.MODE_CBC, key[-32:-16]).decrypt(bytes.fromhex(text[:64])).hex()
  hash2=SHA256.new(bytes.fromhex(text[64:])).hexdigest()
  if hash1 != hash2 :
    print('Corrupt!')
    return
  return rmv_padding(decoded)

def padding(s, n=16):
  l=len(s)
  z=15-len(s)%16
  s=s+'1'
  for i in range(z):
    s=s+'0'
  return s

def rmv_padding(s):
  for i in reversed(range(len(s))):
    # print(s[i])
    if s[i]=='1':
      return s[:i]