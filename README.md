# Alfred, the effective WSGI server

This app contains multiple parts:  
* a barebones WSGI server implementation in wsgi_server.py
* some basic WSGI applications from different web frameworks

Usage:  
```
$ # Run the server and the pyramid web application
$ python web_wsgi.py pyramidapp:app
$ # Run the server and the flask web application
$ python web_wsgi.py flaskapp:app
```
Then go check out your browser at http://localhost:8888/hello, or try manually at
```
$ curl -v http://localhost:8888/hello
```
