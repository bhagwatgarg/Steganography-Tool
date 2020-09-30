import numpy as np
import matplotlib.pyplot as plt

def encrypt(im, msg):
  img=np.copy(im)
  prefix='Visit https://bhagwatgarg.github.io'
  msg=prefix+msg
  length=len(msg)
  # 32 bits kept for length of text
  l_bin=format(length, '032b')
  img=img.reshape((-1))
  for i in range(32):
    if l_bin[i]=='0':
      img[i]-=img[i]%2
    else:
      img[i]-=(img[i]+1)%2
  ind=32
  for i in msg:
    ch=format(ord(i), '08b')
    for c in ch:
      if c=='0':
        img[ind]=abs(img[ind]-img[ind]%2)
      else:
        img[ind]=abs(img[ind]-(img[ind]+1)%2)
      ind+=1
  return img.reshape(im.shape)

def decrypt(img):
  prefix='Visit https://bhagwatgarg.github.io'
  length=''
  img=img.reshape((-1))
  for i in range(32):
    length+=str(img[i]%2)
  length=int(length, 2)
  # print(length)
  msg=''
  ind=32
  for i in range(length):
    a=''
    for j in range(8):
      a+=str(img[ind]%2)
      ind+=1
    a=chr(int(a, 2))
    msg+=a
  if msg[:len(prefix)]!=prefix:
    # print('Corrupt')
    return
  return msg[len(prefix):]