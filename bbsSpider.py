# -*- coding: UTF-8 -*-
'''
    Created on 2017-07-07
    Search and achieve stories lists from any given board in JinJiang anonymous BBS.
    @author: Manyao Peng
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import urllib
import urllib2
import requests
import re
import bbsDatabase
from bs4 import BeautifulSoup

class bbsSpider:

    def __init__(self):
        self.baseURL = "http://bbs.jjwxc.net/"
        self.chineseEncode = "gb2312"
        self.boardNum = 2 #default board No. is 2
        self.pageNum = 1 #default page is the first page
        bbsDatabase.my_connect()
        self.boardOption()
    
    def boardOption(self):
        flag = True
        boards = ["unavailable", "General", "Boys Love", "Reading Comments"]
        
        total_num = len(boards)
        while flag:
            count = 0
            for item in boards:
                count += 1
                print "id:%d  board:%25s" % (count, boards[count-1])
                    
            tip = str("\n\n=========== Enter Board id, Press q to quit ============\n\n")
            id = raw_input(tip)
            if id == "q":
                os.system(r'clear')
                flag = False
                break
            
            int_id = int(id)
            if int_id >= 2 and int_id <= total_num:
                os.system(r'clear')
                self.boardNum = int_id
                self.getDetails()
            else:
                print "invalid id"
                continue
    
    def getHTML(self, urlStr):
        if urlStr == "":
            url = self.baseURL + "board.php?board=" + str(self.boardNum) + "&page=" + str(self.pageNum)
        else:
            url = urlStr
        
        # get html content from the url, fix chinese encode bug
        response = urllib2.urlopen(url)
        html = response.read().decode(self.chineseEncode, 'ignore').encode("utf-8")
        if not html:
            print "load html failed"
            return null
        return html
    
    def removeNoise(self, content):
        # remove &nbsp;
        removeNBSP = re.compile(r"&nbsp;")
        content = re.sub(removeNBSP, " ", content).strip()
        removeAMP = re.compile(r"&amp;")
        content = re.sub(removeAMP, "&", content).strip()
        removeBR = re.compile(r"<br/>")
        content = re.sub(removeBR, "\n", content).strip()
        
        # remove blank line
        removeN = re.compile(r"\n{1,}")
        content = re.sub(removeN, "\n", content).strip()
        return content

    def getMsgList(self):
        content = self.getHTML("")
        stories = []
        bsObj = BeautifulSoup(content, "html.parser") # not lxml

        count = 0
        print "\n*************** Page:%3d ***************\n" % self.pageNum
        for node in bsObj.find_all("a", attrs={"title": True, "href":re.compile(r"show.*?")}):
            stories.append(node["href"])
            title = node.get_text().strip()
            update_time = node["title"]
            bbsDatabase.add(title, update_time)
            count += 1
            print "id:%3d\t\t" % count,
            print title + "--------" + update_time
        
        return stories

    def getDetails(self):
        stories = self.getMsgList()
        if not stories:
            print "no stories"
            return
        
        flag = True
        while flag:
            tip = str("\n\n====================\n +: next page, -: previous, pn: page n, post id to see details, q: quit\n=====================\n\n")
            page = raw_input(tip)
            int_page = self.pageNum
            if page == "q":
                flag = False
                break
            elif page == "+":
                int_page += 1
                if int_page>=1:
                   os.system(r'clear')
                   self.pageNum = int_page
                   stories = self.getMsgList()
                else:
                   print "invalid page number"
                   continue
            elif page == "-":
                int_page -= 1
                if int_page>=1:
                   os.system(r'clear')
                   self.pageNum = int_page
                   stories = self.getMsgList()
                else:
                   print "invalid page number"
                   continue
            elif page[0] == 'p':
                int_page = int(page[1:])
                if int_page>=1:
                   os.system(r'clear')
                   self.pageNum = int_page
                   stories = self.getMsgList()
                else:
                   print "invalid page number"
                   continue
            else:
                post_id = int(page)
                urlstring = self.baseURL + stories[post_id-1]
                content = self.getHTML(urlstring)
                bsObj = BeautifulSoup(content, "html.parser")
                count = 0
                print "\n######################%3d###############################\n" % count
                for node in bsObj.find_all(id="topic"):
                   print node.get_text()
                   count += 1
                   print "\n######################%3d###############################\n" % count

if __name__ == '__main__':
    bbs = bbsSpider()
