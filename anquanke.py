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
	
def main():
	print(1)
	start()
	   
def start():
	'''version = time.time()
	for i in range(1, 3, 1):
		time.sleep(2)
		get_aritcle(10,i,version)'''
	pool = ThreadPool(10)
	pool.map(get_aritcle, range(150))
	
def get_aritcle(page):
	count = 100
	version = time.time()
	r = get_aritcle_list(count,page)
	dic = json.loads(r.text)
	t = int(time.time())
	
	db = pymysql.connect(host='localhost', user='root', password='wjwjwj!@#$%^',port=3306,db='cms')
	data = dic['data']
	for v in data:
		try:
			time.sleep(2)
			content = get_article_content(v['id'])
			print(v['id'])
			sql = 'INSERT INTO log_anquanke(v,id,title,category_name,category_slug,descc,date,time_interval,status,comment,cover,subject,red,type,url,source,fee,origin_author,pv,like_count,liked,tags,nickname,avatar,author,is_favorite,favorite_count,content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			cursor = db.cursor()
			cursor.execute(sql,(version,v['id'],v['title'],v['category_name'],v['category_slug'],v['desc'],v['date'],v['time_interval'],v['status'],v['comment'],v['cover'],v['subject'],v['red'],v['type'],v['url'],v['source'],v['fee'],v['origin_author'],v['pv'],v['like_count'],v['liked'],str(v['tags']),v['author']['nickname'],v['author']['avatar'],str(v['author']),v['is_favorite'],v['favorite_count'],content))
			db.commit()
		except Exception as e:
			#db.close()
			print('%s' %(e))
	db.close()

def get_aritcle_list(count,page):
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
	}
	r = requests.get('https://api.anquanke.com/data/v1/posts?size='+str(count)+'&page='+str(page), headers=headers)
	print('-')
	return r

def get_article_content(id):
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
	}
	r = requests.get('https://www.anquanke.com/post/id/'+str(id), headers=headers)
	html = r.text.encode('utf-8')
	soup = BeautifulSoup(html, 'lxml')
	content = soup.find_all(class_='article-content')
	return content[0].encode('utf-8')

main()
