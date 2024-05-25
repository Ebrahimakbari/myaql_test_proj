import requests
from bs4 import BeautifulSoup
import mysql.connector

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
r = requests.get(
    'https://www.skysports.com/womens-championship-table', headers=header)
soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
main_data = []
for row in rows:
    data = []
    for head in row.select('th'):
        data.append(head.text.replace('\n', ''))
        temp = data
    for body in row.select('td'):
        data.append(body.text.replace('\n', ''))
        temp = data
    main_data.append(temp[0:-1])

mydb = mysql.connector.connect(user='ebrahimak', password='admin@1990', host='localhost')
cursor_a = mydb.cursor()
cursor_a.execute('create database if not exists score')
cursor_a.execute('use score')
cursor_a.execute('create table if not exists scores'
                 '(id int auto_increment primary key,'
                 'number varchar(10),'
                 'team varchar(30),'
                 'p1 varchar(10),'
                 'w varchar(10),'
                 'd varchar(10),'
                 'la varchar(10),'
                 'f varchar(10),'
                 'a varchar(10),'
                 'gd varchar(10),'
                 'pts varchar(10)'
                 ')')
sql = ('insert into scores('
       'number,team,p1,w,d,la,f,a,gd,pts) values('
       '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
cursor_a.executemany(sql, main_data)
mydb.commit()
cursor_a.execute('select * from scores')
scores = cursor_a.fetchall()
cursor_a.close()
mydb.close()