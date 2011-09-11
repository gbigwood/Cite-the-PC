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
        outputtext.append("""
        <html><head><title>Cite The PC</title>
        <link rel="stylesheet" type="text/css" href="/css/citeTPC.css" media="screen" />
        </head><body>""")
        #main body
        outputtext.append(self.createOpeningMessage())
        outputtext.append(self.createLandingForm())
        #footer
        outputtext.append('</body></html>')
        return "\n".join(outputtext)

    def createOpeningMessage(self):
        """
        creates the welcome message
        """
        return """
        <div class="welcome"><h1>Welcome to Cite The PC</h1>
        <p>Ever tried to get a paper published only to be told to reference papers you know were written by the programme committee? 
        Need to suck up to get a paper accepted in your field?
        </p>
        <p>Now with cite the PC its never been easier to cite the programme committee! Simply enter the names of the committee into the box below, to get a returned list of the committee member's papers (with links).
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
    Noshir Contractor Northwestern University</br>
    </div>
    </p>
    </div>
    <div class="submitform">
    <form action="submitMembers" method="post" >
        <p>Enter the members below:</p>
        <textarea cols="60" rows="20" name="membernames"></textarea>
        <p><input type="submit" value="Find Papers"/></p>
    </form>
    </div>
    
    """    

    def submitMembers(self, membernames = None):
        """takes the members passed in from the form and calls the citeTPC code
        """
        #handle the newline character
        membernames = membernames.split(unichr(13))
        membernames = (member.strip("\n") for member in membernames)
        return citeTPC.searchForTPC(membernames)

    submitMembers.exposed = True
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
