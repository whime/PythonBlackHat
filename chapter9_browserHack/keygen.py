from Crypto.PublicKey import RSA

new_key = RSA.generate(2048,e=65537)
public_key=new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM")

print(str(public_key,encoding="utf8"),"\n",str(private_key,encoding="utf8"))