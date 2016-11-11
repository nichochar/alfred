# Alfred, serving you day and night

![alt text](static/alfred_pennyworth.jpg)

> Endure, Master Wayne. Take it. This may not be the server you want, but it's the server you need.

--

This repository is still a work in progress around WSGI servers and applications. You can find here:
* a barebones server implementation: [bare_bones_server.py](bare_bones_server.py)
* a simple, basic WSGI compliant  server implementation: [wsgi_server.py](wsgi_server.py)
* some basic WSGI applications from different web frameworks

### Try it
```bash
$ # Run the server and the pyramid web application
$ python wsgi_server.py pyramidapp:app

$ # Run the server and the flask web application
$ python wsgi_server.py flaskapp:app

$ # Run the bottle app
$ python wsgi_server.py bottleapp:app

$ # Run the Alfred one
$ python wsgi_server.py alfredapp:app
```

For each of these, check out your browser at http://localhost:8888/hello, or curl it manually at
```
$ curl -v http://localhost:8888/hello
```
