from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List,ArrayList
from java.net import URL

import re
from datetime import datetime
from HTMLParser import HTMLParser

"""
a burpsuite extender
use the response of website to generate wordlist of password
"""


class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text=[]

    def handle_data(self, data):
        self.page_text.append(data)

    def handle_comment(self, data):
        self.handle_data(data)

    def strip(self,html):
        self.feed(html)
        return " ".join(self.page_text)


class BurpExtender(IBurpExtender,IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):  # type: (IBurpExtenderCallbacks) -> None
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()

        self.wordlist = {"password"}
        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        return None

    def createMenuItems(self, invocation):  # type: (IContextMenuInvocation) -> List[JMenuItem]
        self.context = invocation
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Create Wordlist",actionPerformed=self.wordlist_menu))
        return menu_list

    def wordlist_menu(self,event):
        http_traffic = self.context.getSelectedMessages()
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            self.hosts.add(host)
            http_response = traffic.getResponse()

            if http_response:
                self.get_words(http_response)
        self.display_wordlist()

    def get_words(self,http_response):
        headers,body = http_response.tostring().split("\r\n\r\n",1)
        if headers.lower().find("content-type: text")==-1: # mind the space between type: and text!!
            return
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)
        words=re.findall("[a-zA-Z]\w{2,}",page_text)
        print("words:", words)
        for word in words:
            if len(word)<=15:
                self.wordlist.add(word.lower())
        return

    def display_wordlist(self):
        print("!comment:BHP wordlist for site(s) %s"%(",".join(self.hosts)))
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)

    def mangle(self,word):
        year = str(datetime.now().year)
        suffixes = ["","1","!",year]
        mangled = []
        for password in (word,word.capitalize()):
            for suffix in suffixes:
                mangled.append(password+suffix)
        return mangled


