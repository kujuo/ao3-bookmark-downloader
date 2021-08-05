import requests
import re
from bs4 import BeautifulSoup
import os
import sys

def getLink(downloadType):
  if downloadType == "pdf": 
    link = soup.select('a[href*="pdf"]')
    secondLink = str(link[0]).replace("<a href=\"", "https://archiveofourown.org") 
    secondLink = secondLink.replace("\">PDF</a>", "") 
  elif downloadType == "azw3": 
    link = soup.select('a[href*="azw3"]')
    secondLink = str(link[0]).replace("<a href=\"", "https://archiveofourown.org") 
    secondLink = secondLink.replace("\">AZW3</a>", "") 
  elif downloadType == "mobi": 
    link = soup.select('a[href*="mobi"]')
    secondLink = str(link[0]).replace("<a href=\"", "https://archiveofourown.org") 
    secondLink = secondLink.replace("\">MOBI</a>", "") 
  elif downloadType == "epub": 
    link = soup.select('a[href*="epub"]')
    secondLink = str(link[0]).replace("<a href=\"", "https://archiveofourown.org") 
    secondLink = secondLink.replace("\">EPUB</a>", "") 
  elif downloadType == "html": 
    link = soup.select('a[href*="html"]')
    secondLink = str(link[0]).replace("<a href=\"", "https://archiveofourown.org") 
    secondLink = secondLink.replace("\">HTML</a>", "") 
  else:
    raise RuntimeError(
      'Invalid format.')
  return secondLink

user = sys.argv[1]
downloadType = sys.argv[2]
downloadType = downloadType.lower()
session = requests.Session()

page = 1

works  = """<a href=\"/works/(\d+)\">([^<>]+)</a>\n\s*?by"""

print("Making directory...")
if not os.path.isdir(user+'_'+downloadType):
    os.mkdir(user+'_'+downloadType)
os.chdir(user+'_'+downloadType)

loop = True
print("Downloading...")
while loop: 
    res = session.get('http://archiveofourown.org/users/'+user+'/bookmarks?page='+str(page))
    html = res.text
    allWorks = re.findall(works, html)
    if len(allWorks) < 1:
      loop = False
    for work in allWorks:
        urlnew = 'http://archiveofourown.org/works/' + work[0]
        r = session.get(urlnew)
        soup = BeautifulSoup(r.text, 'html.parser')

        dlLink = getLink(downloadType)
        filename = soup.title.string.lstrip()
        filename = re.sub(r'(?u)[^-\w.\[\]() ]', '', filename)
        filename = filename[0:filename.find('[')]+"."+downloadType
        ra = requests.get(dlLink, allow_redirects=True)
        open(filename, 'wb').write(ra.content)
        page+=1

print("Done!")