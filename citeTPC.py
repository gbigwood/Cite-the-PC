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

#Make a container type for the pc members
Member = namedtuple('PCMember', ['name', 'institution'])

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


