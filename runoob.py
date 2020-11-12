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
from pathlib import Path
import sys
import http.client
	
def main():
	# 循环站点地图
	pool = ThreadPool(10)
	pool.map(start, range(150))
	
def start(ii):
	try:
		version = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		try:
			html_url = 'https://www.runoob.com'+menu_list[ii].attrs['href']
			type = menu_list[ii].string
			type = type.replace('教程', '');
			type = type.strip()
		except Exception as e:
			print('1.%s' %(e))
			return 1

		# 循环站点地图下的菜单列表
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
		}
		time.sleep(1)
		try:
			r = requests.get(html_url, headers=headers, timeout=30)
		except (ConnectionError, ReadTimeout):
			print('2.Crawling Failed', url)
			return 1

		db = pymysql.connect(host='localhost', user='root', password='wjwjwj!@#$%^',port=3306,db='cms')	
		if r.status_code==200:
			html = r.text.encode('utf-8')
			soup = BeautifulSoup(html, 'lxml')
			menu = soup.select('#leftcolumn a')
			lenth = len(menu)
			for i in range(lenth):
				# 菜单
				title = menu[i].string.strip()#title
				#type_  = title.split(" ", 1)
				#type = type_[0]#type
				# 内容
				content_url_ = menu[i].attrs['href']
				content_url = 'https://www.runoob.com/'+content_url_
				headers = {
					'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
				}
				time.sleep(2)
				try:
					r = requests.get(content_url, headers=headers, timeout=30)
				except Exception as e:
					print('3.%s' %(e))
					continue
				html = r.text.encode('utf-8')
				soup_2 = BeautifulSoup(html, 'lxml')
				content_ = soup_2.select("#content")
				if len(content_)>0:
					content = content_[0].encode('utf-8')#content
				else:
					print('--')
					continue
				# 内容的图片加域名
				content = replace_image_path(content)
				# 入库
				cursor = db.cursor()
				sql = 'INSERT INTO log_runoob(title,v,type,content_url) VALUES (%s,%s,%s,%s)'
				cursor.execute(sql,(title, version, type, content_url_))
				id = db.insert_id()
				sql = 'INSERT INTO log_runoob_data(articleid,content) VALUES (%s,%s)'
				cursor.execute(sql,(id, content))
				db.commit()
				#print(content_url,title,type)
				#quit()
			db.close()
	except Exception as e:
		print('%s' %(e))
		return 1
def replace_image_path(html):
	soup = BeautifulSoup(html, 'lxml')
	# 替换图片连接
	imglist = soup.find_all("img")
	lenth = len(imglist)
	for i in range(lenth):
		try:
			item = imglist[i].attrs['src']
		except Exception as e:
			continue
		item = item.encode('utf-8').strip()
		item = str(item, encoding = "utf-8")
		if not isinstance(html,str):
			html = str(html, encoding = "utf-8")
		if item!='':
			item = item + '"'
			if "www.runoob.com" in item:
				vv333=1
			else:
				new_img_url = "https://www.runoob.com" + item
				html = html.replace(item, new_img_url);
	# 替换a连接
	imglist = soup.find_all("a")
	lenth = len(imglist)
	for i in range(lenth):
		try:
			item = imglist[i].attrs['href']
		except Exception as e:
			continue
		item = item.encode('utf-8').strip()
		item = str(item, encoding = "utf-8")
		if not isinstance(html,str):
			html = str(html, encoding = "utf-8")
		if item!='':
			#print(item)
			item = item + '"'
			if "runoob.com" in item:
				vv333=2
			else:
				new_img_url = "https://www.runoob.com" + item
				html = html.replace(item, new_img_url);
	return html



html_url = 'https://www.runoob.com/sitemap'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}
r = requests.get(html_url, headers=headers, timeout=30)
html = r.text.encode('utf-8')
soup = BeautifulSoup(html, 'lxml')
menu_list = soup.select(".article-body li a")
main()
