# -*- coding: UTF-8 -*-
from wsgiref.validate import validator
import gevent, unittest, urllib2
from summarizer.middleware import SummarizerMiddleware
from gevent import pywsgi
from gevent import monkey

# Monkey patch, so urllib2 works with gevent
monkey.patch_all()

class TestMiddleware(unittest.TestCase):

    @staticmethod
    def application(env, start_response):
        html = open('test/article.html').read()
        start_response('200 OK', [('Content-Type', 'text/plain'),('content-length', str(len(html)))])
        return [html]


    def setUp(self):
        self.app = validator(SummarizerMiddleware(self.application))
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

    def test_summarizer_middleware(self):
        socket = urllib2.urlopen('http://127.0.0.1:15001/article/01.tldr')
        response = socket.read()
        expected = '<!DOCTYPE html><html><head><title>Too Long, Didn\'t read</title></head><body><p>He described the captive as "a former '\
            'employee and a current contractor working with the U.S. government in its aid program to Pakistan, which aims to fight the jihad in '\
            'Pakistan and Afghanistan, and just like the Americans arrest any suspect linked to al Qaeda and the Taliban, even if they were far related."'\
            ' The speaker then listed eight demands that he said, if met, would result in Weinstein\'s release.<bold>They included the lifting of the '\
            'blockade on movement of people and trade between Egypt and Gaza; an end to bombing by the United States and its allies in Pakistan,'\
            ' Afghanistan, Yemen, Somalia and Gaza; the release of anyone arrested on charges of belonging to al Qaeda and the Taliban; '\
            'the release of all prisoners in Guantanamo and American secret prisons and the closure of Guantanamo and the other prisons; '\
            'the release of terrorists convicted in the 1993 bombing of the World Trade Center; and the release of relatives of Osama bin Laden, '\
            'the founder of al Qaeda who was killed in May in Pakistan.</bold>Warren Weinstein is at left with Ali Amjad (center), Mark Wilkinson and Waste '\
            'Management staff members."Your government is torturing our prisoners, and we have never tortured your prisoner," he added.</p></body></html>'

        self.assertEquals(response, expected)
   

