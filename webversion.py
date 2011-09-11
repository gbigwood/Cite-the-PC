"""
The website version of citeTPC
"""
import cherrypy


class LandingPage:
    def index(self):
        return self.createWelcomePage()
    def createWelcomePage(self):
        """
        join a header and a body and a footer together
        """
        header = '<html><head><title>Papers to cite</title></head><body>'
        body = "hi tamsin"
        footer = '</body></html>'
        return header+body+footer

    index.exposed = True
# CherryPy always starts with cherrypy.root when trying to map request URIs
# to objects, so we need to mount a request handler object here. A request
# to '/' will be mapped to cherrypy.root.index().
cherrypy.root = LandingPage()

if __name__ == '__main__':
    # Use the configuration file tutorial.conf.
    cherrypy.config.update(file = 'tutorial.conf')
    # Start the CherryPy server.
    cherrypy.server.start()


