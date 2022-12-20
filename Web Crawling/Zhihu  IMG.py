from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.request import urlretrieve
import os
from func_timeout import func_set_timeout


def get_answer(content : str) -> dict:
    url = "https://www.zhihu.com/search?q=" + content + "&type=content&vertical=answer"
    os.chdir(r"C:\\Program Files\\Google\\Chrome\Application")
    os.system(r'start chrome --remote-debugging-port=58805 --user-data-dir="E:\selenium"')
    os.chdir(r"G:\\VSCode Asset\\python\assert")
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:58805")
    s = Service('chromedriver.exe')
    driver = webdriver.Chrome(service = s,options=options)
    driver.get(url)
    sleep(2)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    url_dict = {}
    for i in range(10):
        script_url = '''
        return document.getElementsByClassName("ContentItem-title")[
        ''' + str(i) + "].children[0].children[0]"
        script_title = '''
        return document.getElementsByClassName("ContentItem-title")[
        ''' + str(i) + "].children[0].children[1]"
        url = driver.execute_script(script_url).get_attribute('content')
        title = driver.execute_script(script_title).get_attribute('content')
        url_dict[title] = url
    driver.quit()
    return url_dict


def choose(url_dict : dict) -> list:
    record = []
    for everykey in url_dict:
        print("其标题为：" + everykey)
        a = input("输入'D'删除该标题,输入其他不删")
        if (a == 'D' or a == 'd'):
            continue
        record.append(url_dict[everykey])
    return record


def get_imgurl(url_answer : list) -> list:
    os.chdir(r"C:\\Program Files\\Google\\Chrome\Application")
    os.system(r'start chrome --remote-debugging-port=58805 --user-data-dir="E:\selenium"')
    os.chdir(r"G:\\VSCode Asset\\python\assert")
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:58805")#这里的port应与上方一致
    s = Service('chromedriver.exe')
    driver = webdriver.Chrome(service = s,options=options)
    url = []
    for i in url_answer:
        driver.get(i)
        # _ = input('输入空格以继续......')
        sleep(3)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        try:
            target = driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[4]")
            sleep(1)
            target.click()
            sleep(0.5)
        except:
            print("无需点击")
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(2)
        driver.execute_script("window.scrollBy(0,-1000)")
        sleep(1)
        for i in range(10):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(2)
        data = driver.find_elements(By.TAG_NAME,'img')
        print("该网页共{}张图片, 正在提取链接".format(len(data)+1))
        for i in range(len(data)):
            temp = data[i].get_attribute('data-original')
            if temp == None:
                temp = data[i].get_attribute('data-default-watermark-src')
            if temp == None:
                continue
            url.append(temp)
    driver.quit()
    return url


@func_set_timeout(2)
def download_pict(url : str, i : int):
    print("正在下载第{}张".format(i+1))
    IMAGE_URL = url
    urlretrieve(IMAGE_URL, 'img' + str(i) + '.jpg')


if __name__ == '__main__':
    content = input("输入你想搜索的内容：")
    list_url = get_imgurl(choose(get_answer(content)))
    for i in list_url:
        try:
            download_pict(list_url[i],i)
        except:
            print("第{}张超时".format(i))
            continue

