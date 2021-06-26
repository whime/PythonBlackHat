import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAoZESfhGcbVFafXYheQu423zXijSAchO7LHdIAGSSvOGG3A5p
y6t4cCzzssgs/NtlJwAOZb6JFNAoo4SxvWkxzmaqTpnDGqV9pzS7aZiyj7g/E7oY
wIX8x5aVmFT3V7b7QXhNYpv0kYveIT5K7rxYmybzmesARiyr3EdT3rUtmOV0TjD9
PIM7v1xLzkI9g12BCqTGhMNsURQ+FZphadh/Cxnvaxbw8NFgXKCbidBvB0sng7iB
my2Fd6mUJkQM5wL7FF/joeVgLX+kirfe9qk0kewSuS3bwMHeKgT6I6uaZf+YVJsd
zD3Pyxe3WX0kYZ3VA8hp1dXfCAR1Cu4iuwTi6QIDAQABAoIBAAK8MwSHLqEdQGDW
hdILXDrfOXutHpT+CT4DN7ciNaCDA+SzFMQI8RGpTu69MRNVxn8F4xT0QQ2Pu1m5
ijeKXGMwC7H9AXQGAFwlprFZXaxGW2utfXsrx7xuCER18qk6AvyfKx1SDRIStZGA
ctQFp/gEqeBaC87kUcOApYLrNDqooKggfmQZsYaPrLsRSEVgp1UwKc5/ZKk3oXDF
F86/eqwooA9UP7f2xY8rxVW+/KaSMtUgSTgo1sku5F7HKf8jgsXGvDCNZwDyB+Ud
90SfZsA3oqciTTFP8dtjIafP5qYyNAZrm1auEK/udxhkTY+vKNdAw4ncVTn4Xa33
JPnN45UCgYEAxYV88VL8BPjWzWAx8nILBinhSBcBFwkNnSX0r/PhM3YeQM1yQKgm
IsYbuB54vURxwGNzsF2bhpq3n8Zn3Y8P2g1V7kghplZbzvO5ks68+tsunjhQUhsG
haz/+jPcImKL4OBhXmDqM4z1rV376aiO5J8xvKhavffnTsYiOyRPwb0CgYEA0WaB
/1P2m1n+xtU6Kj1xai3tj3DVm7PAt2Rk5RzipKKZPx1Z1z/Etnoh4vXY2xuivvuA
okwjabxP33C9uLYsYsrxLKscgM/olxHmrfTj2hH5DFAwj5acvWsYTtf/xDzqLsuP
+nyYvcV1hBVfBsvjwLUhmsktUuwzGW/98anTep0CgYBOpDg7qOuYWy7CtFMOkWNc
P95nImmXr04RTGRgjbwTDis7Z9Ded1Q/shqlMtSlnpOforkT9iEO9Zi4b3k5GFWa
XobhCS0EmguRmS5Aijlps0ybSBaKqiHtpRSBnJY/xnakwRFjTzjP74Z9URcUT70c
v1lBINKIIiShE3fbjjiHDQKBgQC+0HJVgOWP2wpXlaZTJ3paD1ATDfcY00wh0dI/
FXtSGvkaklxz0SAoSFLoxq69uwkqj3RAcLE0gO0n50x7LUZ1IAl1cteeadbBEwbq
LeYTqZ0Qo2Ic9loOIbEc56eh4wBjdAvXbgKhq3XSzsaxIsp/qI7excQPdD18SJlX
xjF34QKBgHiWXjRsXn0gsPRfMY9p87ZmlAD24BTyv44b2hZR4iuoogivuMipjrhp
sCDdyhIziR4Cu4mGJMqiBuIWJDH6+S6BD1hz+931cNdNgO+M+WryxlLYWhE8wvIq
lC/7f6q+y6Eck504YgglUU3es54I4Wmw7npJZePzqRtJ2mcu1B8Z
-----END RSA PRIVATE KEY-----'''
rsakey=RSA.importKey(private_key)
rsakey=PKCS1_OAEP.new(rsakey)

chunk_size=256
offset=0
decrypted=b""
encrypted=b"\x10FJ:\x9d\x9eUw\xfc'\x1ci\xabq\xed\x80i\xbb\x99\xe0\x8c\xcf,\x95O\xb7\xd8\xd0n\xdd\t\x98k\xd4a\xe2RK\xcb\x94\xb9\xc42&\x00\xb8\x1fN\xd9\x94\x90\n\xa6L\x95y\x88\xa6\x83\xc2\xc9+\xb0F\xf0H\x81\x0f}\xb2m\xf6\xda\x0f \x07*\x9d\x19\xe9I\xd2\x82\xdb[\xefy\x04>\x1a\x1b\x9f\xe0\x84\x18\xff\x1a\x9b8P\x01\x8d\xf7\xb5-\x86\x83-\x17\xb5\xbfUzf\x1aG}\xb0cn\xeb.\xb8}^W\x85\x8a\xf6\xc2t\xe4\x90g\xb9(\xda\xe67\xe1\xd5#\xd7\x95\xf4/\xee\xd4\xaf\x16\x98z0\x00\x7f\x1c7\x10\xe2.\x8d3\xa5\xc9\xfc\xd1 \xe5\xfe\xde\xbf\xe0J\xf0n\xab\xed\xd5\xc54\x8aP\x94\x9f\xd7\xa6\x90\x1a\xf31\xc7\xf5\x1c\xed\x9d\xbb\xdd\xccFU\x02(\xf0\x01\xd2*\xaa\xe3\xfb\x03m\xff\xe04\x8f\xf5\x14\xe2c\xc7\xc8:\xce\xc2 \x9e\x19#\xc1\xedc\xef9p\xb6\x19\x88GG\xa9\xb1\xa3\xa4\x18\xfaR\x9f5\xe3\x88<I\xba\xc5\xaa-"
# encrypted=base64.b64decode(encrypted)

while offset<len(encrypted):
    decrypted+=rsakey.decrypt(encrypted[offset:offset+chunk_size])
    offset+=chunk_size
plaintext = zlib.decompress(decrypted)
print(plaintext)
