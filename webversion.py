"""
The website version of citeTPC
"""
import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))
import cherrypy
import citeTPC


class LandingPage:
    def index(self):
        return self.createWelcomePage()
    def createWelcomePage(self):
        """
        join a header and a body and a footer together
        """
        outputtext = []
        #header
        outputtext.append(self.getHeaderText())
        #main body
        outputtext.append(self.createOpeningMessage())
        outputtext.append(self.createLandingForm())
        #footer
        outputtext.append('</body></html>')
        return outputtext#cherrypy will join items for us

    def getHeaderText(self,title="Cite The PC"):
        """gets the page header"""
        #TODO take an optional arguement for the title
        return """
        <html><head><title>%s</title>
        <link rel="stylesheet" type="text/css" href="/css/citeTPC.css" media="screen" />
        </head><body>""" % title

    def createOpeningMessage(self):
        """
        creates the welcome message
        """
        return """
        <div class="welcome">
        <h1>Welcome to Cite The PC</h1>
        <p>Ever tried to get a paper published only to be told to reference papers you know were written by the programme committee? 
        Need to suck up to get a paper accepted in your field?
        </p>
        <p>Now with Cite The PC, it's never been easier to cite the programme committee! Simply enter the names of the committee into the box below, to get a returned list of the committee members' papers (with links).
        </p>
        </div>
        """
    def createLandingForm(self):
        """creates the form that asks for the user details"""
        return """
    <div class="formExplain">
    <p>We could submit a selection of people with names, affiliations or research areas:
        <div class="examplecode">
        Tristan Henderson</br>
        Greg Bigwood University of St Andrews</br>
        Iain Parris Privacy</br>
        </div>
    </p>
    <p>
    Or perhaps an entire list of PC members and their affiliations:
    <div class="examplecode">
    Kevin Almeroth University of California</br>
    Sun-Ki Chai University of Hawaii</br>
    Adrian David Cheok National University of Singapore</br>
    Dongman Lee KAIST</br>
    </div>
    </p>
    </div>
    <div class="submitform">
    <form action="results" method="post" >
        <p><h3>Enter the PC members below:</h3></p>
        <textarea cols="60" rows="20" name="membernames"></textarea>
        <p><input type="submit" value="Find Papers"/></p>
    </form>
    </div>
    
    """    

    def results(self, membernames = None):
        """takes the members passed in from the form and calls the citeTPC code
        """
        #handle the newline character
        membernames = membernames.split(unichr(13))
        membernames = (member.strip("\n") for member in membernames)
        outputtext = []
        outputtext.append(self.getHeaderText(title="Results"))
        outputtext.append("""<h1>Papers to cite</h1>""")
        outputtext.append("\n".join(citeTPC.searchForTPC(membernames)))
        outputtext.append('</body></html>')
        return outputtext

    results.exposed = True
    index.exposed = True


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': True,
                            'engine.autoreload_on':True,
                            })
        
    conf = {'/css': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'data/css'),
                      }}
    cherrypy.quickstart(LandingPage(), '/', config=conf)
