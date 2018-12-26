from pprint import pformat


def hello(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield b'Hello World!'


def application(env, start_response):
    status = '200 OK'
    body = pformat(env).encode('utf-8')

    headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body)))
    ]

    start_response(status, headers)
    return [body]
