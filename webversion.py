"""
The website version of citeTPC
"""
import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))
import cherrypy


class LandingPage:
    def index(self):
        return self.createWelcomePage()
    def createWelcomePage(self):
        """
        join a header and a body and a footer together
        """
        header = """<html><head><title>Papers to cite</title>
        <link rel="stylesheet" type="text/css" href="/css/citeTPC.css" media="screen" />
        </head><body>"""
        body = self.createOpeningMessage()
        footer = '</body></html>'
        return header+body+footer
    def createOpeningMessage(self):
        """
        creates the welcome message
        """
        return """
        <div class="welcome"><h1>Welcome to citeTPC</h1>
        <p>Ever tried to get a paper published only to be told to reference papers you know were written by the programme committee? 
        Need to suck up to get a paper accepted in your field?
        </p>
        <p>Now with citeTPC its never been easier to cite the programme committee! Simply enter the names of the committee into the box below, to get a returned list of the committee member's papers.
        </p>
        </div>
        """

    index.exposed = True

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': True})
        
    conf = {'/css': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'data/css'),
                      }}
    cherrypy.quickstart(LandingPage(), '/', config=conf)
