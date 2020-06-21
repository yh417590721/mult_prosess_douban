import multiprocessing
from datetime import time
from multiprocessing import Manager
import requests
from bs4 import BeautifulSoup
import pandas as pd

from multiprocessing import Process




def request_douban(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None





def save_to_excel(soup):

    list = soup.find(class_='grid_view').find_all('li')

    for item in list:
        movie_list = []  # 这里定义一个空list
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        if (item.find(class_='inq') != None):
            item_intr = item.find(class_='inq').string

        # print('爬取电影：' + item_index + ' | ' + item_name +' | ' + item_img +' | ' + item_score +' | ' + item_author +' | ' + item_intr )
        print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intr +'|'+item_author)

#从这里开始修改


        movie_list.append([item_name,item_img,item_index,item_score,item_author,item_intr]) #list添加一条记录
    return movie_list





def main(url,mlist):
    html = request_douban(url)
    soup = BeautifulSoup(html, 'html.parser')
    save_to_excel(soup,mlist)


if __name__ == '__main__':
    #start = time.time()

    movie_list = Manager().list()
    urls = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(0, 10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
        urls.append(url)
    pool.map(main,urls)
    pool.close()
    pool.join()


    file_save = pd.DataFrame(movie_list,columns=['名称','图片','排名','评分','作者','简介'])
    file_save.to_csv('豆瓣5.csv',index=None,encoding='utf_8_sig')




