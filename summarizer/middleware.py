
from webob import Request
from summarizer import summarize
from nltk.util import clean_html
import re


class SummarizerMiddleware(object):
    """ WSGI Middleware runs HTML documents through a text summarizer if
    the path ends in .tldr

    Attempts to summarize the HTML document by searching for frequently
    occuring words and selecting the sentence with the highest frequency of
    common words as the summary

    num_summaries - The total number of summary sentences output on the
                    summary
    page num_context_sentences - Number of sentences that make up
                                 the context of the summary sentence

    """

    def __init__(self, app, num_summaries=1, num_context_sentences=2):
        self.context = num_context_sentences
        self.number = num_summaries
        self.app = app

    def summary_html(self, summaries):
        body = ['<!DOCTYPE html>', '<html>', '<head><title>Too Long, Didn\'t '
                'read</title></head>', '<body>']
        # Iterate through the summaries
        for key in summaries.keys():
            paragraph = []
            # Get the sentences with context
            for sentence in summaries[key]:
                if sentence == key:
                    # The summary sentence should stand out
                    paragraph.append('<bold>%s</bold>' % sentence)
                else:
                    paragraph.append(sentence)
            # Append the paragraph to the body
            body.append("<p>%s</p>" % ''.join(paragraph))

        body.append("</body></html>")
        return ''.join(body)

    def __call__(self, env, start_response):
        # While not nessary, webob makes this easy
        request = Request(env)
        # Call up the middleware pipeline
        response = request.get_response(self.app)

        # Is the body HTML? (This assumes, our wsgi app is doing sane things
        # and setting a DOCTYPE)
        if re.match('\s*?<!DOCTYPE\s*?html', response.body):
            # If the PATH ends in .tldr
            if re.search('\.tldr\s*?$', request.path):
                # Summarize the html
                response.body = self.summary_html(
                    summarize(self.number,
                              self.context,
                              clean_html(response.body)))

        return response(env, start_response)
