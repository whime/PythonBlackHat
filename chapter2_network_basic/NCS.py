import sys
import socket
import getopt
import threading
import subprocess

"""
@author: whime
@description:NCS, Netcat_simulator, to simulate some functions of Netcat
just have fun!!!
@Notes: 
1.characters to graphs:http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
2.In py3,make a distinction between bytes and str
"""


# TODO(must unify all the encoding mode for all the widget)


class NCS():
    listen = False
    command = False
    upload = False
    execute = ""
    target = ""
    port = 0
    upload_destination = ""
    upload_source=""

    def __init__(self,encoding="gbk"):
        self.encoding = encoding

    def usage(self):
        print("NNNNNNNN        NNNNNNNN        CCCCCCCCCCCCC   SSSSSSSSSSSSSSS\n"
              "N:::::::N       N::::::N     CCC::::::::::::C SS:::::::::::::::S\n"
              "N::::::::N      N::::::N   CC:::::::::::::::CS:::::SSSSSS::::::S\n"
              "N:::::::::N     N::::::N  C:::::CCCCCCCC::::CS:::::S     SSSSSSS\n"
              "N::::::::::N    N::::::N C:::::C       CCCCCCS:::::S\n"
              "N:::::::::::N   N::::::NC:::::C              S:::::S\n"
              "N:::::::N::::N  N::::::NC:::::C               S::::SSSS\n"
              "N::::::N N::::N N::::::NC:::::C                SS::::::SSSSS\n"
              "N::::::N  N::::N:::::::NC:::::C                  SSS::::::::SS\n"
              "N::::::N   N:::::::::::NC:::::C                     SSSSSS::::S\n"
              "N::::::N    N::::::::::NC:::::C                          S:::::S\n"
              "N::::::N     N:::::::::N C:::::C       CCCCCC            S:::::S\n"
              "N::::::N      N::::::::N  C:::::CCCCCCCC::::CSSSSSSS     S:::::S\n"
              "N::::::N       N:::::::N   CC:::::::::::::::CS::::::SSSSSS:::::S\n"
              "N::::::N        N::::::N     CCC::::::::::::CS:::::::::::::::SS\n"
              "NNNNNNNN         NNNNNNN        CCCCCCCCCCCCC SSSSSSSSSSSSSSS \n")
        print("\n\nusage:NCS.py -t target_host -p port\n")
        print("options:\n"
              "-l --listen                      listen on [host]:[port] for incoming connections\n"
              "-e  --execute                    execute the given file upon receive a connection\n"
              "-c --command                     return a command console\n"
              '-u --upload                      format "file1>file2",the upload source file to destination file\n'
              "\n"
              "Examples:\n"
              "NCS.py -t 192.168.0.1 -p 9999 -l -c\n"
              "NCS.py -t 192.168.0.1 -p 9999 -l -e=\"ls -la\"\n"
              "NCS.py -t 192.168.0.1 -p 9999 -l --upload='file1>file2'\n")
        sys.exit(0)

    def run(self):  # run as a server or client

        if len(sys.argv) == 1:
            self.usage()

        # parser options
        try:
            options, args = getopt.getopt(sys.argv[1:], "t:p:lcu:e:h",
                                          ["target=", "port=", "listen", "command", "upload=", "execute=",
                                           "help"])
        except getopt.GetoptError as e:
            print(e)
            self.usage()

        for opt, arg in options:
            if opt in ["-h", "--help"]:
                self.usage()
            elif opt in ["-p", "--port"]:
                NCS.port = int(arg)
            elif opt in ["-l", "--listen"]:
                NCS.listen = True
            elif opt in ["-c", "--command"]:
                NCS.command = True
            elif opt in ["-u", "--upload"]:
                NCS.upload_source = arg.split(">")[0]
                NCS.upload_destination = arg.split(">")[1]
            elif opt in ["-e", "--execute"]:
                NCS.execute = arg
            elif opt in ["-t", "--target"]:
                NCS.target = arg
            else:
                assert False, "parse options error!!"
                # raise AssertionError("parse options error!!!")
        if not NCS.listen and NCS.target != "" and NCS.port > 0:
            # run as client and send command to server,end with ctrl-D
            # just read stdin and send!
            # buffer = sys.stdin.read()
            self.client_sender()

        if NCS.listen:
            # run as a server and wait for connect
            self.server_loop()

    def client_sender(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # try to connect to server:
        try:
            client_socket.connect((NCS.target, NCS.port))
        except Exception as e:
            print(e)
            client_socket.close()

        if NCS.upload_source:
            # to upload file
            with open(NCS.upload_source, "rb") as f:
                data = f.read()
                client_socket.send(data)
            upload_response = ""
            while True:
                res = client_socket.recv(1024).decode(encoding=self.encoding)
                upload_response += res
                if len(res) < 1024:
                    break
            print(upload_response)

        # wait,receive response from server,and print
        label = True  # if receive label 'ncs/>' or result of executed command
        while True:
            response = ""
            while True:
                data = client_socket.recv(4096).decode(encoding=self.encoding)
                data_len = len(data)
                response += data

                if data_len < 4096:
                    break
            if label:
                print(response, end="")
                label = not label
            else:
                print(response)
                response = ""
                while True:
                    data = client_socket.recv(4096).decode(encoding=self.encoding)
                    data_len = len(data)
                    response += data

                    if data_len < 4096:
                        break
                print(response,end="")

            # wait for more console input
            buffer = input("")
            buffer += "\n"

            client_socket.send(buffer.encode(encoding=self.encoding))

    def server_loop(self):
        # default listen all interfaces if not define target
        if len(NCS.target) == 0:
            NCS.target = "0.0.0.0"

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((NCS.target, NCS.port))
        server_socket.listen(5)  # accept 5 connections at most

        while True:
            client_socket, addr = server_socket.accept()
            print(str(addr)+" connected")
            # start a new thread to handle the new connection
            handle_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            handle_thread.start()

    # deal with the connection of client
    def handle_client(self, client_socket):

        # upload file to specific pathname
        if len(NCS.upload_destination):
            file_buffer = ""
            while True:
                data_seg = client_socket.recv(1024).decode(encoding=self.encoding)
                file_buffer += data_seg
                if len(data_seg) < 1024:
                    break

            # write to file
            try:
                with open(NCS.upload_destination, "w") as f:
                    f.write(file_buffer)
                client_socket.send(
                    ("successfully saved file to %s\n" % NCS.upload_destination).encode(encoding=self.encoding))
            except Exception as e:
                client_socket.send(("failed to save file!\n" + str(e)).encode(encoding=self.encoding))

        # if need to execute a command and send the result to client
        if len(NCS.execute):
            # start a new thread to execute the command,otherwise the server thread will block here,like open a Notepad program
            execute_thread=threading.Thread(target=self.execute_command,args=(NCS.execute,))
            execute_thread.start() # no result feed back to client

        # if need to imitate a interactive console to client
        if NCS.command:
            while True:
                client_socket.send(bytes("NCS/>:", encoding=self.encoding))
                console_buffer = ""
                # receive data stream ends with carry return
                while "\n" not in console_buffer:
                    console_buffer += client_socket.recv(1024).decode(encoding=self.encoding)
                # print(bytes(console_buffer, encoding=self.encoding))

                output = self.execute_command(console_buffer)

                client_socket.send(output)

    # use a subprocess to execute command and return result
    def execute_command(self, cmd):
        cmd = cmd.rstrip()
        try:
            # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)
            process = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
            output = process.stdout.read()
        except Exception as e:
            output = str(e).encode(self.encoding)
        return output


if __name__ == '__main__':
    ncs = NCS()
    ncs.run()