from selenium import webdriver
from queue import PriorityQueue
import threading
from Crypto.Hash import keccak
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

Queuelock = threading.Lock()
Hashlock = threading.Lock()

URLList = {}

class Trie :
    def __init__(self):
        self.go = {}
        self.fail = self
        self.output = False

class Node :
    def __init__(self,url,weight):
        self.url = urlparse(url)
        self.pweight = weight
        self.seeds = ""

    def Calculate_Weight(self):
        self.nweight = 0;

    def GetWeight(self):
        return self.pweight

    def work(self):
        self.list = []
        driver = webdriver.Chrome('/Users/user/Downloads/chromedriver_win32/chromedriver.exe')
        driver.get(self.url.geturl())
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        self.seeds = [tag.name for tag in soup.findAll()]
        self.Calculate_Weight()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.close()

class Crawler:

    global lock
    def Manage(self):
        start_time = time.time()
        while True :
            Queuelock.acquire()
            if self.que.empty() == False :
                node = self.que.get()[1]
                print(self.que.qsize())
                thread = threading.Thread(target=node.work)
                thread.start()
                Queuelock.release()
            else :
                if time.time() - start_time > 30:
                    print(time.time()-start_time)
                    break
                Queuelock.release()
                time.sleep(0.01)


    def __init__(self):
        self.que = PriorityQueue()
        self.thread = threading.Thread(target=self.Manage)
        self.thread.start()

    """
        Only Use this in function where QueueLock is used
    """
    def add_Queue(self,node):
        self.que.put((node.GetWeight(),node))


