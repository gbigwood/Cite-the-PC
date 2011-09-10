"""
A program to obtain a list of all the papers that you need to cite to get
accepted at your conference.
 __
/  \        _____________
|  |       /             \
@  @       | It looks    |
|| ||      | like you    |
|| ||   <--| are writing |
|\_/|      | a paper.    |
\___/      \_____________/
"""
from BeautifulSoup import BeautifulSoup
from collections import namedtuple
import urllib2
#The hardcoded strings for tags
paperContainer = "gs_r"
linkToPaper = "gs_ggs"

#Make a container type for the pc members
Member = namedtuple('PCMember', ['name', 'institution'])

#who we are searching for
listofnames = [
    Member("Kevin Almeroth", "University of California"),
    Member("Sun-Ki Chai", "University of Hawaii"),
    Member("Adrian David Cheok", "National University of Singapore"),
    Member("Noshir Contractor", "Northwestern University"),
    Member("Irfan Essa", "Georgia Institute of Technology"),
    Member("David Lazer", "Northeastern/Harvard University"),
    Member("Dongman Lee", "KAIST"),
    Member("Ramesh Jain", "University of California"),
    Member("Tom Malone", "Massachusetts Institute of Technology"),
    Member("Kenji Mase", "Nagoya University"),
]

### Create opener with Google-friendly user agent
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

url = "http://scholar.google.com/scholar?q=Kevin+Almeroth+University+of+California"
page = opener.open(url)
soup = BeautifulSoup(page)


#print soup.prettify()
#Parse and find the gs_r tags
for cite in soup.findAll(name='div',attrs={"class" : paperContainer}):
    print cite.div.a #contains the link to the paper page
    if linkToPaper in cite.span['class']: # contains a link to the hardcopy
        print cite.span.a
