def app(environ, start_response):
    """A Barebones WSGI application

    Starting point of our loyal server
    """
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world from Alfred WSGI application\n']
