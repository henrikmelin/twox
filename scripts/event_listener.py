#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer, urlparse, twox

class TWOXlistener(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        
        # Get the query variables
        args = urlparse.parse_qs(urlparse.urlparse(self.path).query)        
        
        # We need an event to process
        if ('event' not in args) : 
            self.wfile.write('0')
            return False
        if ('value' not in args) : args['value'] = ['']

        # Pull out event name and value and process it
        event = args['event'][0]
        value = args['value'][0]
        helper = twox.twox()
        ret = helper.process_event(event, value)

        # Provide some feedback on the request
        output = '0' 
        if (ret == True) : output = '1'
        self.wfile.write(output)

if __name__ == "__main__":
    httpd = HTTPServer(('', 8081), TWOXlistener)
    print 'Listening on :8081...'
    httpd.serve_forever()
    