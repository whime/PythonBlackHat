import threading
import socket
import sys

"""
@author:whime
@description:a proxy to transfer traffic:   localClient<=>TCP_proxy<=>remote_server
"""


class tcpProxy:
    def __init__(self, encoding="utf8"):
        self.encoding = encoding

    def run(self):
        if len(sys.argv[1:]) != 5:
            print("Usage:tcpProxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first")
            print("Example:tcpProxy.py 127.0.0.1 9999 10.1.1.2 8888 True")
            sys.exit()

        local_host = sys.argv[1]
        local_port = int(sys.argv[2])
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])

        receive_first = True if "True" in sys.argv[5] else False
        self.server_loop(local_host, local_port, remote_host, remote_port, receive_first)

    # proxy service main loop
    def server_loop(self, local_host, local_port, remote_host, remote_port, receive_first):

        proxyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            proxyServer.bind((local_host, local_port))
        except Exception as e:
            print("Failed to listen on %s:%d" % (local_host, local_port))
            print(e)
            sys.exit(0)

        print("start listening on %s:%d" % (local_host, local_port))

        proxyServer.listen(5)  # accept 5 connection at most
        while True:
            client_socket, addr = proxyServer.accept()
            print("[==>]received incoming connection from %s:%d" % (addr[0], addr[1]))
            proxy_thread = threading.Thread(target=self.proxy_handler,
                                            args=(client_socket, remote_host, remote_port, receive_first))
            proxy_thread.start()

    def proxy_handler(self, client_socket, remote_host, remote_port, receive_first):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        # receive from remote server first?
        if receive_first:
            data = self.receive_from(remote_socket)
            self.hexDump(data)

            remote_data = self.response_handler(data)
            if len(remote_data):
                print("[<==]sending %d bytes to localhost" % len(remote_data))
                client_socket.send(remote_data.encode(self.encoding))

        while True:
            local_data = self.receive_from(client_socket)

            if len(local_data):
                print("received %d bytes from localhost" % (len(local_data)))
                self.hexDump(local_data)
                local_data = self.request_handler(local_data)
                remote_socket.send(local_data.encode(self.encoding))
                print("[==>]send to remote")

            remote_data = self.receive_from(remote_socket)
            if len(remote_data):
                print("[<==]received %d bytes from remote" % len(remote_data))

                self.hexDump(remote_data)
                remote_data = self.response_handler(remote_data)

                client_socket.send(remote_data.encode(self.encoding))
                print("[<==] send to localhost")

            if not len(local_data) and not len(remote_data):
                client_socket.close()
                remote_socket.close()
                print("[*]No more data,Closing connections")

                break

    def receive_from(self, connection):
        data = ""
        connection.settimeout(10)

        try:
            while True:
                dataTmp = connection.recv(4096)
                if not dataTmp:
                    break
                data += dataTmp.decode(encoding=self.encoding)

        except Exception as e:
            print(e)
        return data

    def hexDump(self, src, length=16):
        result = []
        digits = 4 if isinstance(src, str) else 2

        print("\n")
        for i in range(0, len(src), length):
            s = src[i:i + length]
            hexa = " ".join(["%0*X" % (digits, ord(x)) for x in s])
            text = "".join([x if 0x20 <= ord(x) < 0x7F else "." for x in s])
            result.append("%04X    %-*s    %s" % (i, length * (digits + 1), hexa, text))

        print(("\n".join(result)))

    def request_handler(self, request):
        return request

    def response_handler(self, response):
        return response


if __name__ == '__main__':
    proxy = tcpProxy()
    proxy.run()