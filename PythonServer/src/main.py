import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from index import app

'''class MainHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

application = tornado.web.Application([  
    (r"/",MainHandler),  
]) '''

http_server = HTTPServer(WSGIContainer(app))
#application.listen(5000)
http_server.listen(5000)
IOLoop.instance().start()
