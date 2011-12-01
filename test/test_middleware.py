from wsgiref.validate import validator
import gevent, unittest, urllib2
import summarizer.middleware
from gevent import pywsgi
from gevent import monkey

# Monkey patch to urllib2 works with gevent
monkey.patch_all()

class TestMiddleware(unittest.TestCase):

    @staticmethod
    def application(env, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain'),('content-length', '16')])
        return ['wsgi hello world']


    def setUp(self):
        self.app = validator(self.application)
        self.server = pywsgi.WSGIServer(('127.0.0.1', 15001), self.app)
        self.server.start()
        self.port = self.server.server_port


    def tearDown(self):
        timeout = gevent.Timeout(0.5,RuntimeError("Timeout trying to stop server"))
        timeout.start()
        try:
            self.server.stop()
        finally:
            timeout.cancel()

    def test_wsgi_server(self):
        response = urllib2.urlopen('http://127.0.0.1:15001/')
        self.assertEquals(response.read(), 'wsgi hello world')
   

