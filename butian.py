# -*- coding: utf-8 -*-
import sys    
import time
import random
import requests
from bs4 import BeautifulSoup
from requests import exceptions 
import threadpool
import re
import json

reload(sys)    
sys.setdefaultencoding('utf8')

#define some global variables using for the url request
data={
	'Host': 'butian.360.cn',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie': 'test_cookie_enable=null; __utma=148900148.587966501.1509193630.1509193630.1509193630.1; NTKF_T2D_CLIENTID=guest8EE3D616-67D6-EC59-64B7-5E5808EAAD24; __huid=10Qx1U4SbHO4eZgKERtMZ36CnlwB%2BCHvfUzvJKCThSVMY%3D; __guid=233952199.869463173871049984.1534952583000.7751; PHPSESSID=s5ebri3ju0fvcg4qmv4is85247; Q=u%3D360H3098325487%26n%3D%26le%3D%26m%3DZGt5WGWOWGWOWGWOWGWOWGWOAQRl%26qid%3D3098325487%26im%3D1_t01923d359dad425928%26src%3Dpcw_webscan%26t%3D1; _currentUrl_=%2FMessage; quCapStyle=2; __gid=192414782.165403898.1509116348611.1545561731160.105; quCryptCode=D6TqMQxFspnphxHSGa34EucJhnkfgqks62eHgLADFzlEvFq06UiWICX5fSny9cnYqrqgcfxszGI%253D; T=s%3D4b752402d305f6d3d7f5d21239ccfd6b%26t%3D1546226098%26lm%3D%26lf%3D2%26sk%3Da520b70cb7aa66750defba5f754b0be5%26mt%3D1546226098%26rc%3D%26v%3D2.0%26a%3D1; test_cookie_enable=null; __DC_sid=138613664.3257148641371525600.1546319851524.4536; __DC_monitor_count=43; __DC_gid=192414782.165403898.1509116348611.1546320460264.389; __q__=1546320460432',
        'Referer': 'http://butian.360.cn/Reward/plan'}
#proxie=[{"http": "183.136.218.253:80"},{"http": "14.215.177.73:80"},{"http": "14.215.177.58:80"},{"http": "163.177.151.23:80"},{"http": "112.80.255.21:80"},{"http": "121.8.98.198:80"},{"http": "112.80.255.32:80"},{"http": "220.181.163.231:80"},{"http": "202.100.83.139:80"},{"http": "115.239.210.42:80"},{"http": "123.125.115.86:80"},{"http": "123.125.142.40:80"},{"http": "163.177.151.162:80"},{"http": "60.2.148.253:80"}]
user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like GeckoChrome/22.0.1207.1 Safari/537.1","Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5","Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)Chrome/19.0.1061.0 Safari/536.3","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"]

class butiansrc(): #定义爬取及处理

	def domain(self,result):   #对域名进行处理
		#if 'www' in result:
		#	result=result.replace('www.','')
		#if 'http://' in result:
		#	result=result.replace('http://','')
		#if 'https://' in result:
		#	result=result.replace('https://','')
		#if '/' in result:
		#	result=result.replace('/','')
		result=result+"\n"
                http_result="http://"+result
                https_result="https://"+result
                all_result=result+http_result+https_result
		open('domain.txt','ab').write(all_result) # 保存全部域名


	def urlresult(self,url):
                global data, user_agent_list
		result=''					    #对url进行爬取
		#aproxie=proxie[random.randint(0,10)]
		data['User-Agent']=user_agent_list[random.randint(0,18)]
		#try:
                print 'make request'
		getre=requests.get(url,headers=data)
		#getre=requests.get(url,headers=data,proxies = aproxie)
		soup = BeautifulSoup(getre.text,'html.parser')
		result=unicode(soup.find_all('input')[4]['value'])
		#except:
                #        print "except happened"
		#	pass
		if result !='':
			self.domain(result)

class create(): #定义任务开始

	def __init__ (self):
                print 'step 1. get the src cids'
                #header={'Accept':'application/json'}
                #url_corps="http://butian.360.cn/Reward/corps"
                #data_json={'s':3,'p':1,'sort':1,'token':''}
                #res=requests.post(url_corps, headers=header, data=data_json)
                f=open('SRC.html', 'r')
                res=f.read()
                f.close()
                #soup=BeautifulSoup(res,'html.parser')
                #print(soup.find_all(href=re.compile('\/Loo\/submit\?cid=[0-9]{1,8}')))
                cids=re.findall('cid=[0-9]{1,8}', res)
                str_cids=''
                for i in cids:
                    str_cids+=i+","

                self.cids=re.findall('[0-9]{1,8}',str_cids)
                

	def url_list(self):
                print 'step 2. construct the urls using cids'
		urls=[]
		for i in self.cids:
			url="http://butian.360.cn/Loo/submit?cid="+i  #创建url列表
			urls.append(url)
		return urls

	def useing(self):
                print 'step 3. start thread pool to request urls and parse the responses'
		url_list=self.url_list()
		pool=threadpool.ThreadPool(5)
	        butianobj=butiansrc()
                print 'create thread pool'
                start_time = time.time()
                works = threadpool.makeRequests(butianobj.urlresult,url_list)
		[pool.putRequest(req) for req in works]   #构建线程池
		pool.wait()
                print '%d seconds elapsed' % (time.time() - start_time)
		

if __name__ == "__main__":  # start
	print 'start-----------------'
	start=create()   
	start.useing()
		
