from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os

#下面的指令尽量在cmd里面运行，在本程序运行时需加入以下代码:
#其中port后面的数字可以自己设定 以下只做参考
#os.chdir(r"C:\\Program Files\\Google\\Chrome\Application")
#os.system(r'chrome --remote-debugging-port=58805 --user-data-dir="E:\selenium"')
#input('输入空格以继续......')

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:58805")#这里的port应与上方一致
s = Service('chromedriver.exe')
browser = webdriver.Chrome(service = s,options=options)

#由于知乎存在异步加载情况 故需多次鼠标下滑
for i in range(10):
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(0.5)

#整理字符串得到数据
string = ""
data = browser.find_elements(By.TAG_NAME,'p')
for i in range(len(data)):
    string = string + data[i].text

print(string)


