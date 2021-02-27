import random
import json
from Crypto.Util.Padding import pad,unpad
from Crypto.Cipher import AES,DES
from base64 import b64encode,b64decode

# 金智AES加密
def wiseduAES(data, key):
    encrypted = aesEncrypt(randomString(64) + data, key, randomString(16))
    return encrypted

# 获取指定长度字符串
def randomString(length):
    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    retStr = ''
    for i in range(length):
        retStr += random.choice(chars)
    return retStr

# AES加密
def aesEncrypt(data0, key0, iv0):
    data  = data0.encode('utf-8')
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    return ct

# AES解密
def aesDecrypt(data0, key0, iv0):
    data  = data0.encode('utf-8')
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    ct = b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

# DES加密
def desEncrypt(data0, key0, iv0):
    data  = data0.encode('utf-8')
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    cipher = DES.new(key, DES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data, DES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    return ct

# DES解密
def desDecrypt(data0, key0, iv0):
    data  = data0.encode('utf-8')
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    ct = b64decode(data)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), DES.block_size)
    return pt



