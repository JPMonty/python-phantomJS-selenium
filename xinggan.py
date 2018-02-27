from selenium import webdriver  # 导入Selenium
import requests
from bs4 import BeautifulSoup  # 导入BeautifulSoup 模块
import os  # 导入os模块
import time


class BeautifulPicture():

    def __init__(self, web_url):  # 类的初始化操作

        self.driver = webdriver.PhantomJS()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}  # 给请求指定一个请求头来模拟chrome浏览器

        self.web_url = web_url  # 要访问的网页地址

        self.folder_path = '/Users/zhumengdi/xinggan/'  # 设置图片要存放的文件目录

        self.cookies = '';



    def get_pic(self, href):
        driver = self.driver
        driver.get(href)
        self.cookies = driver.get_cookies()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        content_pic = soup.find('div', {'class', 'content-pic'})
        img = None
        if content_pic:
            img = content_pic.find('img')
        if not img:
            return;
        next = soup.find('a', string='下一页')
        url = img['src']
        file_name = img['alt'] + '.jpg'

        file_names = self.get_files(self.folder_path)  # 获取文件家中的所有文件名，类型是list

        if is_new_folder:
            self.save_img(url, file_name)  # 调用save_img方法来保存图片
        else:
            if file_name not in file_names:
                self.save_img(url, file_name)  # 调用save_img方法来保存图片
            else:
                print("该图片已经存在：", file_name, "，不再重新下载。")
        if next:
            self.get_pic(self.web_url + next['href'])



    def index(self):
        print('开始网页get请求')
        # 使用selenium通过PhantomJS来进行网络请求
        driver = self.driver
        driver.get(self.web_url)
        # self.scroll_down(driver, 3)  #执行网页下拉到底部操作，执行3次

        print('开始获取所有img标签')
        self.cookies = driver.get_cookies()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        dl = soup.find('dl', {'class': 'list-left public-box'})
        if not dl:
            return;
        # all_img = dl.find_all('img')  #获取网页中的class为cV68d的所有img标签
        all_a = dl.find_all('a')

        for a in all_a:
            self.get_pic(a['href'])

        next_url = soup.find('a', text='下一页')
        print("下一页:" + next_url['href'])

        if next_url['href']:
            BeautifulPicture.index(self.web_url + next_url['href'])

    def save_img(self, url, file_name):  ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功！')
        f.close()

    def request(self, url):  # 返回网页的response
        url = url.lstrip('/')
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        self.headers['Referer'] = self.web_url

        cookies = dict()
        for cookie in self.cookies:
            name = cookie['name']
            value = cookie['value']
            cookies[name] = value

        r = requests.get(url, cookies=cookies, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def scroll_down(self, driver, times):
        pass
        # for i in range(times):
        # print("开始执行第", str(i + 1),"次下拉操作")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #执行JavaScript实现网页下拉倒底部
        # print("第", str(i + 1), "次下拉操作执行完毕")
        # print("第", str(i + 1), "次等待网页加载......")
        # time.sleep(5)  # 等待30秒，页面加载出来再执行下拉操作

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names




beauty = BeautifulPicture(web_url='http://www.mm131.com/xinggan/')  # 创建类的实例

print('开始创建文件夹')
is_new_folder = beauty.mkdir(beauty.folder_path)  # 创建文件夹，并判断是否是新创建

print('开始切换文件夹')
os.chdir(beauty.folder_path)  # 切换路径至上面创建的文件夹

beauty.index()  # 执行类中的方法
