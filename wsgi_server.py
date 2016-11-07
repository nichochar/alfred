import socket
import StringIO
import sys


RECEIVE_BYTES = 1024
SERVER_ADDRESS = (HOST, PORT) = '', 8888


class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)

        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind
        listen_socket.bind(server_address)

        # Activate
        listen_socket.listen(self.request_queue_size)

        # Get server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        # Return headers set by Web framework/Web application
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            # Initialize client connection
            self.client_connection, client_address = listen_socket.accept()
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(RECEIVE_BYTES)
        # Print formatted request data a la 'curl -v'
        print (''.join('< {line}\n'.format(line=line) for line in request_data.splitlines()))

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # Call our application callable and get back the response body
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)

    def parse_request(self, text_req):
        request_line = text_req.splitlines()[0]
        request_line = request_line.rstrip('\r\n')

        # Break down the request line into components
        (self.request_method,  # GET
         self.path,            # /hello
         self.request_version  # HTTP/1.1
         ) = request_line.split()

    def get_environ(self):
        env = {}
        required_WSGI_vars = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO.StringIO(self.request_data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False
        }
        required_CGI_vars = {
            'REQUEST_METHOD': self.request_method,  # GET
            'PATH_INFO': self.path,                 # /hello
            'SERVER_NAME': self.server_name,        # localhost
            'SERVER_PORT': str(self.server_port)    # 8888
        }
        env.update(required_WSGI_vars)
        env.update(required_CGI_vars)

        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Sun, 6 Nov 2016 11:51 PST'),
            ('Server', 'Alfred WSGI 0.1')]
        self.headers_set = [status, response_headers + server_headers]
        # To follow WSGI spec, the start_response must return a 'write' callable.
        # For simplicity we will ignore for now
        return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data

            # Print formatted response data a la 'curl -v'
            print ''.join('> {line}\n'.format(line=line) for line in response.splitlines())
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()


def make_server(server_address, application):
    """Initialize the WSGIServer and pass it the application object
    Args
    ----
    server_address: <tuple> of (host, port) like ('', 8888)
    application: the WSGI compatible application object

    Returns
    -------
    A WSGI standard server object
    """
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print 'WSGIServer: Serving HTTP on port  {port} ...\n'.format(port=PORT)
    httpd.serve_forever()
