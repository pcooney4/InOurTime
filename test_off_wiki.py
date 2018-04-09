try:
    # Python 3.x
    from urllib.request import urlopen, urlretrieve, quote
    from urllib.parse import urljoin
except ImportError:
    # Python 2.x
    from urllib import urlopen, urlretrieve, quote
    from urlparse import urljoin

def find_between( s, first, last ):
    try:
#: and - screwing up data parser..
	s = s.replace("-", " ")
        s = s.replace(":", " ")
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_In_Our_Time_programmes'
u = urlopen(url)
try:
    html = u.read().decode('utf-8')
finally:
    u.close()
soup = BeautifulSoup(html, "html.parser")

result = []
bdate = []
import sys, importlib, glob
import dateutil.parser as dparser
import os.path
time = importlib.import_module("time")
foo = 0

for link in soup.find_all(class_="external text"):
    href = link.get('href')
    href = href.replace("//", "/")
    href = href.replace("http:/", "http://")
    if href.startswith("http://www.bbc.co.uk/programmes/"):
         if not glob.glob('*' + str(href)[-8:] + '*'):
              datestr = dparser.parse(find_between(str(link), '>', '</a>'), fuzzy=True)
              result.append(str(href))
              bdate.append(str('{:%Y-%m-%d}'.format(datestr)))
         else:
              print "Skipping http://www.bbc.co.uk/programmes/" + str(href)[-8:] + "."
 
for x in result:
    start_time = time.time()
    url = x
    u = urlopen(url)
    try:
         html = u.read().decode('utf-8')
    finally:
         u.close()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find(class_="link-complex br-linkinvert buttons__download__link")
    if link != None:
         href = link.get('href')
         filename = link.get('download')
         if os.path.isfile(filename):
              print "Skipping " + filename + "."   
         else:
              filename = filename.replace("/", "-")
              urlretrieve(href, bdate[foo] + " " + filename)
              elapsed_time = time.time() - start_time
              print "Downloaded " + filename + " in " + str(round(elapsed_time)) + " seconds."
    foo += 1
