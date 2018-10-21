# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import requests
import re
from bs4 import BeautifulSoup

URL = "http://bbs.jjwxc.net/board.php?board=3"
# get html content from the url, fix chinese encode bug
html = urllib2.urlopen(URL).read().decode("gb2312", 'ignore').encode("utf-8")
if not html:
  print "load html failed"
stories = []
bsObj = BeautifulSoup(html, "html.parser") # not lxml
for node in bsObj.find_all("a", attrs={"title": True, "href":re.compile(r"show.*?")}):
    stories.append(node["href"])
    print(node.get_text().strip() + "--------" + node["title"])
for story in stories:
    print(story)
