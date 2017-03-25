def aplication(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return 'Hello, %s!' % environ['PATH_INFO'][1:] or 'web'
