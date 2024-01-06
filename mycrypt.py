from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from config import *

def encrypt(plaintext, key=key):
    # 生成一个随机的初始向量
    iv = get_random_bytes(AES.block_size)

    # 创建一个AES cipher对象，使用CFB模式
    cipher = AES.new(key, AES.MODE_CFB, iv)

    # 加密明文
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))

    # 将初始向量附加到密文前面，然后使用base64编码，便于存储和传输
    encrypted_data = base64.b64encode(iv + ciphertext).decode('utf-8')

    return encrypted_data

def decrypt(encrypted_data, key=key):
    # 对加密数据进行base64解码
    encrypted_data_bytes = base64.b64decode(encrypted_data)

    # 分离初始向量和密文
    iv = encrypted_data_bytes[:AES.block_size]
    ciphertext = encrypted_data_bytes[AES.block_size:]

    # 创建一个AES cipher对象，使用CFB模式
    cipher = AES.new(key, AES.MODE_CFB, iv)

    # 解密密文
    decrypted_data = cipher.decrypt(ciphertext).decode('utf-8')

    return decrypted_data