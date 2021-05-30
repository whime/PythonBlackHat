**web_app_mapper.py**
+ install and configure CMS joomla in vm host 192.168.29.128,and after delete installation directory
+ download and decompress Joomla_3.9.27-Stable-Full_Package.zip in localhost
+ run script in localhost to test the CMS according to the content of joomla package
+ all file can be accessed except files under directory "installation",returning code 404
!["code 200"](../imgs/web_mapper_200.png)
!["code 404"](../imgs/web_mapper_404.png)
!["CMS joomla"](../imgs/cms_joomla.png)

**content_bruter**

using Dictionary all.txt to perform dirBruter.

!["dirBruter"](../imgs/dirBruter.png)

**joomla_kill.py**
+ It is a script that using wordlist to bruteforce administrator login page of joomla CMS.
+ It saves the cookies,parse the hidden form element,and extract some key-value especial a random token
+ with a given username and a wordlist of password,send a post request and verify whether the password is correct.
!["joomla_login_page"](../imgs/joomla_login_page.png)
!["administrator_page_title"](../imgs/administrator_page_title.png)
!["joomla_bruteforce_success"](../imgs/joomla_bruteforce_success.png)

That's all. 

