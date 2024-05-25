import requests
from bs4 import BeautifulSoup
import mysql.connector

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
r = requests.get('https://news.ycombinator.com/', headers=header)
soup = BeautifulSoup(r.text, 'html.parser')
results = []
for line in soup.findAll('tr', class_='athing'):
    temp_list1 = line.get_text('*').split('*')
    link = line.css.select_one('td span a').get('href')
    temp_list = line.find_next_sibling('tr').get_text('*').split('*')
    results.append((temp_list1[3], link, ' '.join(
        temp_list[3:5]), temp_list[-3].replace('\xa0', ' ')))

mydb = mysql.connector.connect(
    user='@@', password='@@', host='@@')
cursor = mydb.cursor()
cursor.execute('create database if not exists news')
cursor.execute('use news')
cursor.execute('create table if not exists data(id int auto_increment primary key,'
               'title varchar(100),'
               'link varchar(200),'
               'writer varchar(50),'
               'comment_count varchar(50))')
sql = 'insert into data (title,link,writer,comment_count) values(%s,%s,%s,%s)'
cursor.executemany(sql, results)
mydb.commit()
cursor.close()
mydb.close()
