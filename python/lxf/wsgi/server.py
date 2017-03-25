from wsgiref.simple_server import make_server
from hello import aplication

server = make_server('', 9000, aplication)
print 'Serve port on 9000'
server.serve_forever()
