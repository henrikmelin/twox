#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer, urlparse

class TWOXhandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        # If we need to have vars defined, override this...
        self.set_vars()
        
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
        ret = self.event_handler(event, value)
		
        # Provide some feedback on the request
        output = '0' 
        if (ret == True) : output = '1'
        self.wfile.write(output)

	def event_handler(self, event, value) : 
		print("Class method not overridden!")
		return False	
	
	def set_vars() :
	    return False

def start_event_server(handler, port=8081) : 
	httpd = HTTPServer(('', port), handler)
	print("Starting httpd server on " + str(port))
	httpd.serve_forever()



    