import requests
import threading
import queue

threads = 5
target_url = "http://testphp.vulnweb.com"
# download from https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/
wordlist_file = "./all.txt"
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"


def build_wordlist(worldlist_file):
    with open(wordlist_file,"r") as f:
        raw_words = f.readlines()
    words = queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        words.put(word)
    return words


def dir_bruter(word_queue,extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []
        if "." not in attempt:
            attempt_list.append("/%s/"%attempt)
        else:
            attempt_list.append("/%s"%attempt)

        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s"%(attempt,extension))

        for brute in attempt_list:
            url = "%s%s"%(target_url,requests.utils.quote(brute))
            try:
                headers = {"User-Agent": user_agent}
                response = requests.get(url,headers=headers)
                if response.status_code == 200:
                    print("200 =>%s"%url)
            except Exception as e:
                if hasattr(e,'code') and e.code != 404:
                    print("exception")
                    # print("!!!%d =>%s"%(e.code,url))
                    pass


if __name__ == '__main__':
    word_queue = build_wordlist(wordlist_file)
    extensions = [".php",".bak","orig","inc"]

    for i in range(threads):
        t = threading.Thread(target=dir_bruter,args=(word_queue,extensions))
        t.start()


