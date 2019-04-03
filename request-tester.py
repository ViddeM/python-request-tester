import pprint

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class LogginMiddleWare(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self.app(environ, log_response)

@app.route('/', methods=['GET', 'POST'])
def parse_request():
    url = request.url
    encoding = str(request.content_encoding)
    length = str(request.content_length)
    data = str(request.data)
    header = str(request.headers)

    #print("url: " + url + "\n encoding: " + encoding + "\n length: " + length + "\n data: " + data + "\n header: " + header)

    return "success!"


if __name__ == '__main__':
    app.wsgi_app = LogginMiddleWare(app.wsgi_app)
    app.run(host='0.0.0.0')