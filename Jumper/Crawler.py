from selenium import webdriver
from queue import PriorityQueue
import threading
from Crypto.Hash import keccak
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import asyncio

URLList = {}
OrgSeeds = []
class Trie :
    def __init__(self):
        self.go = {}
        self.fail = self
        self.output = False

class Node :
    def __init__(self,url,weight,type):
        self.url = urlparse(url)
        self.pweight = weight
        self.type = type

    def __lt__(self, other):
        return self.pweight < other.pweight

    def Calculate_Weight(self):
        global OrgSeeds
        n = len(self.seeds)
        m = len(OrgSeeds)
        lcs = [[0 for _ in range(m+1)] for _ in range(n+1)]
        for i in range(1,n+1):
            for p in range(1,m+1):
                if self.seeds[i-1]==OrgSeeds[p-1] :
                    lcs[i][p] = lcs[i-1][p-1] + 1;
                else:
                    lcs[i][p] = max(lcs[i-1][p],lcs[i][p-1])
        self.nweight = lcs[n][m]/max(n,m)


    def GetWeight(self):
        return self.pweight

    async def booting(self):
        self.driver = webdriver.Chrome('/Users/user/Downloads/chromedriver_win32/chromedriver.exe')
        self.driver.get(self.url.geturl())

    async def scrolling(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    async def work(self):
        global OrgSeeds
        self.Nodelist = []
        boot = asyncio.create_task(
            self.booting()
        )
        await boot
        """
        boot_selenium = asyncio.get_event_loop()
        boot_selenium.run_until_complete(self.booting())
        """
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        self.seeds = [tag.name for tag in soup.findAll()]
        if self.type == 0:
            OrgSeeds = self.seeds
        self.Calculate_Weight()
        scroll = asyncio.create_task(
            self.scrolling()
        )
        await scroll
        Gobox = self.driver.find_elements_by_partial_link_text('a')
        for i in range(len(Gobox)) :
            nexturl = Gobox[i].get_attribute('href')
            tmp = urlparse(nexturl)
            nexturl = tmp.geturl()
            if type(nexturl) is str and nexturl.startswith("http"):
                hashurl = keccak.new(digest_bits=256)
                hashurl.update(nexturl.encode('utf-8'))
                if hashurl.hexdigest() not in URLList:
                    print(nexturl)
                    nextNode = Node(nexturl,self.nweight,1)
                    self.Nodelist.append(nextNode)
                    URLList[hashurl.hexdigest()] = nexturl

        self.driver.close()
        return self.Nodelist

class Crawler:
    global lock
    async def Manage(self):
        start_time = time.time()
        node = Node(self.first_data, 100000000,0)
        self.add_Queue(node)
        while True :
            if self.que.empty() == False :
                start_time = time.time()
                node = self.que.get()
                task = asyncio.create_task(
                    node.work()
                )
                NextNodeList = await task
                for i in range(len(NextNodeList)):
                    self.add_Queue(NextNodeList[i])
            else :
                if time.time() - start_time > 30:
                    print(time.time()-start_time)
                    break
                time.sleep(0.01)


    def __init__(self,data):
        self.first_data = data
        self.que = PriorityQueue()
        asyncio.run(self.Manage())


    def add_Queue(self,node):
        self.que.put(node)


