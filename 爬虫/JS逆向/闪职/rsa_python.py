from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as cry_pk
import base64

def encrypt(pk, password):
    """
    python重构RSA加密
    :param pk: 公钥
    :param password: 需要加密的明文密码
    :return: 加密之后的秘闻密码
    """
    public_key = "-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----".format(pk)
    # 导入公钥  返回一个rsa密钥对象
    rsakey = RSA.importKey(public_key)
    # 对需要加密内容进行
    cipher = cry_pk.new(rsakey)
    # 使用公钥加密密码 密码必须是二进制
    # print(password.encode())
    # exit()
    miwen_encode = cipher.encrypt(password.encode())
    # 再使用Base64对类似字节的对象进行编码
    cipher_text = base64.b64encode(miwen_encode).decode()
    # 将二进制数据转为字符串
    # print(type(cipher_text), type(cipher_text.decode()))
    return cipher_text


pak = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDaP+rYm6rqTMP565UmMU6YXq46KtAN3zwDSO8LNa15p0lJfsaY8jXY7iLsZqQZrGYr2Aayp6hYZy+Q+AMB/VUiSpD9ojPyOQ7r9jsf9jZbTOL4kj6iLZn37fEhp4eLvRgy5EJCyQoFyLCsgLechBTlYl2eA95C3j4ZUFhiV6WFHQIDAQAB"
new_password = password = encrypt(pak, '123456')
# print(new_password)
