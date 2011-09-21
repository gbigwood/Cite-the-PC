Cite the PC
===========
A command line and web app to find the papers you need to cite to get your paper published.
Ever tried to get a paper published only to be told to reference papers you
know were written by the programme committee? Need to suck up to get a paper
accepted in your field?

Now with Cite The PC, it's never been easier to cite the programme committee!
Simply enter the names of the committee into the box below, to get a returned
list of the committee members' papers (with links and BibTeX).

Requirements
============
It requires:

* python 

The following python modules are also required:

* cherrypy
* beautiful soup

These can (probably) be installed on your system using easyinstall:

	`sudo easy_install cherrypy`

Explanation:
============
We could submit a selection of people with names, affiliations or research areas:

	Tristan Henderson
	Greg Bigwood University of St Andrews
	Iain Parris Privacy

Or perhaps an entire list of PC members and their affiliations:

	Kevin Almeroth University of California
	Sun-Ki Chai University of Hawaii
	Adrian David Cheok National University of Singapore
	Dongman Lee KAIST

Usage:
============
The testinput file includes the PC for ACM SIGCOMM 2011.

Command line version:
---------------------
(The command line version does not require cherrypy.)
The following will output an html file of papers for you to read:

	`< testinput python citeTPC.py > /tmp/papers.html`

Web version:
------------
To run the cherrypy webserver on your machine for use from a browser, simply run:

	`python webversion.py`
This will start the application which you can connect to in your browser at:

	`127.0.0.1:8080`

Results are displayed in the browser.
