#coding:utf-8

import urllib
import urllib2
import re
import thread
import time

#糗事百科爬虫类
class QSBK:
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
        #初始化headers
        self.headers = {'User-Agent' : self.user_agent}
        #放段子的变量，每个元素视每一页的段子们
        self.stories = []
        #存放程序能否继续运行的变量
        self.enable = False
    
    #传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
         try:
             url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
             #构建请求的request
             request = urllib2.Request(url, headers = self.headers)
             #利用urlopen获取页面代码
             response = urllib2.urlopen(request)
             pageCode = response.read().decode('utf-8')
             return pageCode
         except urllib2.URLError,e:
             if(hasattr(e,'reason')):
                 print u"连接糗事百科失败，错误原因",e.reason
                 return None
             
    # 传入某一页的代码
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败..."
            return None
        pattern = re.compile('<div.*?author.*?>.*?<h2>(.*?)</h2>.*?<div.*?content.*?>(.*?)</div>.*?<i.*?number.*?>(.*?)</i>', re.S)
        items = re.findall(pattern, pageCode)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item[1])
            #item[0]式段子的作者， item[1]是段子的内容， item[2]是段子的点赞数
            pageStories.append([item[0].strip(),text.strip(),item[2].strip()])
        return pageStories
    
    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新的一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    
    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载页面
            self.loadPage()
            #如果输入Q，程序退出
            if input == "Q":
                self.enable = False
                return
            #print u"第%d页\t发布人:%s\n内容:%s\n赞:%s" %(page, story[0],story[1],story[2])
            print u"-------------------------------------------------------------------------------"
            print u"第%d页\t发布人:%s\n" %(page, story[0])
            print u"内容:\t%s\n" % story[1]
            print u"赞:%s" % story[2]
            
            
    #开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        #是变量为True.程序可以正常运行
        self.enable = True
        #先加载 一页的内容
        self.loadPage()
        #局部变量，控制当前度到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页 的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)
                
spider = QSBK()
spider.start()
    
    
    
    
    
    
    
                
                
                
                