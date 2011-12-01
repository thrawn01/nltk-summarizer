
from webob import Request
import summarizer
import re


class SummarizerMiddleware(object):
    """ WSGI Middleware runs HTML documents through a text summarizer if the path ends in .tldr """


    def __init__(self, app):
        self.app = app


    def __call__(self, env, start_response):
        # While not nessary, webob makes this easy
        request = Request(env)
        # Call up the middleware pipeline
        resp = request.get_response(self.app)
       
        # Is the response body HTML? 
        # This assumes, our wsgi app is doing sane things and setting a DOCTYPE
        if re.match('<!DOCTYPE\W*?html', string):
            # If the PATH ends in .tldr
            if re.match('\.tldr\W?$', resp.path):
                # Summarize the html
                resp.body = summarize_html(resp.body)

        # Pass on the return value
        return resp(env, start_response)


