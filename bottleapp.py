from bottle import Bottle

app = Bottle()


@app.route('/hello')
def hello():
    return 'Hello world from Bottle!\n'
