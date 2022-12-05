#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests as rq
import pandas as pd
from const import TOKEN, TIME_NOW, VERSION
import datetime as dt
import time


class VkGroup:
    def __init__(self):
        self.group_id = None
        self.screen_name = None
        self.name = None
        self.posts = []

    def __str__(self):
        return f'ID: {self.group_id}\n' \
               f'Domain: {self.screen_name}\n' \
               f'Name: {self.name}\n' \
               f'Members: {self.members}\n'

    def __repr__(self):
        return (f'id={self.group_id}, '
                f'screen_name="{self.screen_name}", '
                f'members={self.members}')

    def __call__(self, group_id=int):
        self.group_id = group_id
        request = rq.get('https://api.vk.com/method/groups.getById',
                         params={
                             'access_token': TOKEN,
                             'v': VERSION,
                             'group_id': self.group_id,
                             'fields': 'members_count'
                         }).json().get('response', None)
        response = request[0]
        self.screen_name = response['screen_name']
        self.name = response['name']
        self.members = response['members_count']

    def get_posts_by_count(self, count=20):
        print('Собираю посты')
        offset = 0

        def request(count=20, offset=0):
            response = rq.get("https://api.vk.com/method/wall.get",
                              params={
                                  'access_token': TOKEN,
                                  'v': VERSION,
                                  'owner_id': -self.group_id,
                                  'count': count,
                                  'offset': offset
                              }).json()['response']['items']
            return response

        if count <= 100:
            self.posts = request(count, offset)
        else:
            while offset < count:
                self.posts.extend(request(100, offset))
                offset += 100
                time.sleep(0.5)
        return pd.DataFrame(self.posts)

    def get_posts_by_date(self, start_date=str, end_date=str):  #
        start_date = dt.datetime.strptime(start_date, "%d-%m-%Y")
        start_date = dt.datetime.timestamp(start_date)
        end_date = dt.datetime.strptime(end_date, "%d-%m-%Y")
        end_date = dt.datetime.timestamp(end_date)
        print(start_date, end_date)

        response = rq.get("https://api.vk.com/method/wall.get",
                          params={
                              'access_token': TOKEN,
                              'v': VERSION,
                              'owner_id': -self.group_id,
                              'count': 100,
                              'offset': 0
                          }).json()['response']['items']

        posts = pd.DataFrame(response)
        index_date = posts[(posts['date'] <= start_date)].index
        posts.drop(index_date, inplace=True)
        index_date = posts[(posts['date'] >= end_date)].index
        posts.drop(index_date, inplace=True)
        self.posts = posts
        print(f'Количество постов за период: {len(self.posts)}')
        return self.posts.sort_values(by=['id'])

    def get_report(self):
        print('Готовлю отчёт...')
        post = self.posts
        post = pd.DataFrame(post)
        try:
            post = post.drop(columns=['from_id', 'marked_as_ads', 'is_pinned',
                                      'edited', 'post_type', 'attachments',
                                      'post_source', 'donut', 'short_text_rate',
                                      'hash', 'carousel_offset', 'copy_history'], axis=1)
        except KeyError:
            post = post.drop(columns=['from_id', 'marked_as_ads', 'is_pinned',
                                      'edited', 'post_type', 'attachments',
                                      'post_source', 'donut', 'short_text_rate',
                                      'hash', 'carousel_offset'], axis=1)
        finally:
            post.insert(1, 'link', "NaN")
            post['owner_id'] = abs(post['owner_id'])
            post['link'] = post.apply(lambda x: f'https://vk.com/wall-{self.group_id}_{x["id"]}', axis=1)
            post['date'] = pd.to_datetime(post['date'], unit='s')
            post['comments'] = post.apply(lambda x: x['comments']['count'], axis=1)
            post['reposts'] = post.apply(lambda x: x['reposts']['count'], axis=1)
            post['likes'] = post.apply(lambda x: x['likes']['count'], axis=1)
            post['views'] = post.apply(lambda x: x['views']['count'], axis=1)
            print('Отчёт готов')
            post.sort_values(by=['id'])
            post.to_excel(f'./{self.name}_posts_{TIME_NOW}.xlsx', header=True, index=False)

    def get_members(self):
        print('Начинаю парсинг подписчиков. Это может занять пару минут...')
        offset = 0
        count = 1
        iteration = 0
        members = []

        while offset < count:
            request = rq.get('https://api.vk.com/method/groups.getMembers',
                             params={
                                 'access_token': TOKEN,
                                 'v': VERSION,
                                 'group_id': self.group_id,
                                 'offset': offset
                             }).json()['response']
            count = request['count']
            offset += 1000
            members.extend(request['items'])
            iteration += 1
            if iteration % 5 == 0:
                time.sleep(0.5)
                continue
        df = pd.DataFrame(members, columns=[f'{self.screen_name}_members_id'])
        df.to_csv(f'./{self.screen_name}_members.csv', header=True, index=False)
        print(f'Парсинг закончен. Подписчиков собрано: {len(members)}. Отчёт готов!')

    def get_id(self, screen_name=str):
        response = rq.get('https://api.vk.com/method/utils.resolveScreenName',
                          params={
                              'access_token': TOKEN,
                              'v': VERSION,
                              'screen_name': screen_name
                          }).json()['response']
        return response['object_id']
