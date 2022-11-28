#!/usr/bin/python3
# -*- coding: utf-8 -*-

# импорты
import csv
import requests
import datetime
import pandas

# вводим глобальные переменные
token = "fcf784d2fcf784d2fcf784d206ffe7472fffcf7fcf784d29fdf12d1cff39e144bbbaa42"
version = 5.131
domain = "welltex"
owner_id = -22564985
count = 100
offset = 0
all_posts = []
time_now = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

# получаем последние посты, кол-во постов равно переменной count


def get_posts():
    response = requests.get("https://api.vk.com/method/wall.get",  # направляем запрос к API VK
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': count,
                                'offset': offset
                                }
                            )
    data = response.json()['response']['items']
    all_posts.extend(data)
    return all_posts


'''
генерируем файл с ID постов, числом лайков, комментариев, репостов и просмотров
'''


def file_generator(all_posts):
    with open('report_' + f'{time_now}' + '.csv',
              mode='w', newline='') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('link', 'ID', 'date', 'likes', 'comments', 'reposts', 'views'))
        for post in all_posts:
            a_pen.writerow(('https://vk.com/wall'+f'{owner_id}'+'_',
                            post['id'],
                            post['date'],
                            post['likes']['count'],
                            post['comments']['count'],
                            post['reposts']['count'],
                            post['views']['count']
                            ))


all_posts = get_posts()
file_generator(all_posts)

if __name__ == '__main__':
    print('The report was created')
else:
    print('error')
