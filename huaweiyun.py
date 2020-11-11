#!C:\Python35
#-*- coding:utf-8 -*-

from urllib import request,error,parse
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import requests
import pymysql
import json
import time
import os 
from hashlib import md5
from multiprocessing.dummy import Pool as ThreadPool
os.path
from pathlib import Path
import sys
	
def main():
	start()
	   
def start():
	pool = ThreadPool(20)
	pool.map(get_aritcle, range(6580,6582))
	
def get_aritcle(page):
	version = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	r = get_aritcle_list(page)
	time.sleep(1)
	if r.status_code==200:
		db = pymysql.connect(host='localhost', user='root', password='123456',port=3306,db='cms')
		html = r.text.encode('utf-8')
		soup = BeautifulSoup(html, 'lxml')
		for i in soup.findAll(class_='blog_whole_area_click'):
			try:
				id = i.attrs['blogid'].strip()#id
				title = i.attrs['bi_title'].strip()#title
				descc_ = i.select(".common-blog-text")
				href = i.select("a")
				descc = i.select('.common-blog-text')
				desc = descc[0].string.strip()
				html_url = href[0].attrs['href'].strip()
				time.sleep(2)
				d = get_article_content(html_url)#content
				time.sleep(1)
				cursor = db.cursor()
				sql = 'INSERT INTO log_huaweiyun(id,title,v,author,date,descc) VALUES (%s,%s,%s,%s,%s,%s)'
				cursor.execute(sql,(id, title, version,d['author'], d['date'],desc))
				sql = 'INSERT INTO log_huaweiyun_data(articleid,content) VALUES (%s,%s)'
				cursor.execute(sql,(id, d['content']))
				db.commit()
				#quit()
			except Exception as e:
				#db.close()
				print('%s' %(e))
		db.close()

def get_aritcle_list(page):
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
	}
	data = {'pageNo':page, 'type':3 }
	r = requests.post('https://bbs.huaweicloud.com/api/rest/front/community/get_blog_list_by_type', data, headers=headers)
	return r

def get_article_content(html_url):
	html_url = 'https://bbs.huaweicloud.com'+html_url
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
	}
	r = requests.get(html_url, headers=headers)
	html = r.text.encode('utf-8')
	soup = BeautifulSoup(html, 'lxml')
	author_ = soup.select(".sub-content-username")
	author = author_[0].string.strip()#author
	date_ = soup.select(".article-write-time")
	date__ = date_[0].string.strip().split(" ", 1)
	date = date__[1]#date
	content_ = soup.select(".cloud-blog-detail-content")
	content = content_[0].encode('utf-8')#content
	content = replace_image_path(content)
	dict = {'author':author, 'date':date, 'content':content}
	return dict
	
def replace_image_path(html):
	base_path = os.path.split(os.path.realpath(__file__))[0]
	year = time.strftime("%Y", time.localtime()) 
	mouth = time.strftime("%m", time.localtime()) 
	day = time.strftime("%d", time.localtime()) 
	img_path = os.path.join('huaweiyun',year, mouth, day)
	if os.path.isdir(img_path):
		a=1
	else:
		os.makedirs(img_path)
	soup = BeautifulSoup(html, 'lxml')
	imglist = soup.find_all("img")
	lenth = len(imglist)
	for i in range(lenth):
		item = imglist[i].attrs['src']
		item = item.strip()
		if item!='':
			x = item.strip().split("?", 1)
			y = item.strip().split("#", 1)
			img_url = x[0]
			if len(y)==2:
				img_url = y[0]
			filename = os.path.basename(img_url)
			new_img_url = os.path.join(base_path, img_path, filename)
			#print(new_img_url)
			r = requests.get(item)
			with open(new_img_url, 'wb') as f:
				f.write(r.content)
			#print(type(html))
			if not isinstance(html,str):
				html = str(html, encoding = "utf-8")
			html = html.replace(item, os.path.join('\\static\\',img_path, filename));
	return html

main()
