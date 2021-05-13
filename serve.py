from http.server import HTTPServer, BaseHTTPRequestHandler
from time import gmtime, strftime
from callback import callback

QUIET=True
def prn(*args):
    if not(QUIET): print (*args)

class Server(BaseHTTPRequestHandler):

    def log_request(self, val):
        pass

    def printRequest(self, method, path):
        prn(strftime("%H:%M:%S", gmtime()), method, path)

    def printHeaders(self, headers):
        prn("HEADERS...")
        for header in str(headers).split("\n"):
            prn("   ", header)

    def send_default_response(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.printRequest("GET", self.path)
        self.printHeaders(self.headers)
        self.send_default_response()
        auth = str(self.headers['Authorization'])
        ip = self.client_address[0]
        callback({ 'protocol': "GET", 'auth':auth, 'ip':ip })

    def do_OPTIONS(self):
        self.printRequest("OPTIONS", self.path)
        self.printHeaders(self.headers)
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_POST(self):
        self.printRequest("POST", self.path)
        self.printHeaders(self.headers)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')
        auth = str(self.headers['Authorization'])
        self.send_default_response()
        ip = self.client_address[0]
        callback({ 'protocol': "POST", 'auth':auth, 'data':data, 'ip':ip })

def serve(port=7777):
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)
    prn("Serving on port", port)
    httpd.serve_forever()

if __name__ == '__main__':
    QUIET=True
    from sys import argv
    if len(argv) == 2:
        serve(port=int(argv[1]))
    else:
        serve()