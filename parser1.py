#!/usr/bin/python3
# -*- coding: utf-8 -*-

#импорты
import time
import csv

import requests

token = "fcf784d2fcf784d2fcf784d206ffe7472fffcf7fcf784d29fdf12d1cff39e144bbbaa42"
version = 5.131
domain = "welltex_perm"
owner_id = -145456773
count = 10
offset = 0

#получаем последние посты, кол-во постов равно переменной count
def get_posts():
    all_posts = []

    response = requests.get ("https://api.vk.com/method/wall.get", #направляем запрос к API VK
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

#генерируем файл со ID постов, числом лайков, комментариев, репостов и просмотров
def file_generator(all_posts):
    with open('test.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('ID','Лайки','Комментарии','Репосты'))
        for post in all_posts:
            a_pen.writerow((post['id'],
                            post['likes']['count'],
                            post['comments']['count'],
                            post['reposts']['count'],
                            post['views']['count']
                            ))

all_posts = get_posts()
file_generator(all_posts)
