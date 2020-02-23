#!/usr/bin/python3

import sys, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

def parseArgs():
    parser = argparse.ArgumentParser(description='For test API Client, webhook, ... ')
    parser.add_argument('-p', '--port', help='Port to listen', dest='port', type=int, required=True)
    parser.add_argument('--host', help='Server address', dest='host', default='')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', dest='verbosity', action='count')
    args = parser.parse_args()

    global PORT
    PORT = args.port
    global HOST
    HOST = args.host
    global VERBOSITY
    if(isinstance(args.verbosity, int)):
        VERBOSITY = int(args.verbosity)
    else:
        VERBOSITY = 0

    if(PORT == None or PORT <=0):
        parser.print_help()
        exit()

def printRequest(request):
    if(VERBOSITY > 0):
        print('FROM: '+request.client_address[0]+':'+str(request.client_address[1])+' ----- ')
        print(request.requestline)
        print(request.headers)
    content_len = int(request.headers.get('Content-Length', 0))
    if(content_len > 0):
        print(request.rfile.read(content_len))

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        printRequest(self)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
        printRequest(self)

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        printRequest(self)

def main():
    parseArgs()
    try:
        print('Open listening for ' + HOST + ':' + str(PORT))
        print('')
        httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        httpd.cgi_directories = ['/']
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutdown requested ... Bye.")
    sys.exit(0)
    

if(__name__ == "__main__"):
    main()
