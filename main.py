import requests
import re
from bs4 import BeautifulSoup
import os
import sys

user = sys.argv[1]
session = requests.Session()

page = 1

works  = """<a href=\"/works/(\d+)\">([^<>]+)</a>\n\s*?by"""

print("Making directory...")
if not os.path.isdir(user):
    os.mkdir(user)
os.chdir(user)

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
        pdflink = soup.select('a[href*="pdf"]')
        pdflin = str(pdflink[0]).replace("<a href=\"", "https://archiveofourown.org") 
        pdflin = pdflin.replace("\">PDF</a>", "")
        filename = soup.title.string.lstrip()
        filename = re.sub(r'(?u)[^-\w.\[\]() ]', '', filename)
        filename = filename[0:filename.find('[')]+".pdf"
        ra = requests.get(pdflin, allow_redirects=True)
        open(filename, 'wb').write(ra.content)
        page+=1

print("Done!")