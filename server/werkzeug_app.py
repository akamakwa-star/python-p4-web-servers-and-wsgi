#!/usr/bin/env python3
"""Simple WSGI app using Werkzeug when available, otherwise wsgiref fallback.

This file attempts to use Werkzeug's `Request`/`Response` and `run_simple` when
`werkzeug` is installed. If it's not available, it provides a pure-stdlib WSGI
application and starts it with `wsgiref.simple_server` so the script works
without extra dependencies.
"""

try:
    from werkzeug.wrappers import Request, Response
    from werkzeug.serving import run_simple

    @Request.application
    def application(request):
        print(f'This web server is running at {request.remote_addr}')
        return Response('A WSGI generated this response!')

    def serve():
        # use positional args to be compatible with different Werkzeug versions
        run_simple('localhost', 5555, application)

except Exception:
    # Fallback to stdlib wsgiref when Werkzeug isn't available
    def application(environ, start_response):
        remote = environ.get('REMOTE_ADDR', '-')
        print(f'This web server is running at {remote}')
        body = b'A WSGI generated this response!'
        headers = [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Content-Length', str(len(body)))
        ]
        start_response('200 OK', headers)
        return [body]

    def serve():
        from wsgiref.simple_server import make_server
        srv = make_server('localhost', 5555, application)
        print('Serving on http://localhost:5555 (wsgiref)')
        srv.serve_forever()


if __name__ == '__main__':
    serve()
