#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import requests as rq
import pandas as pd
from app.src.const import TOKEN, TIME_NOW, VERSION
import datetime as dt
import time
import numpy as np


class VkGroup:
    def __init__(self):
        self.group_id = None
        self.screen_name = None
        self.name = None
        self.posts_per_period = None
        self.posts = []

    def __str__(self):
        return f'{self.name}\n' \
               f'Кол-во подписчиков: {self.members}\n' \
               f'Постов за период: {self.posts_per_period}\n'

    def __repr__(self):
        return (f'id={self.group_id}, '
                f'name="{self.name}", '
                f'screen_name="{self.screen_name}", '
                f'members={self.members}, '
                f'posts_per_period={self.posts_per_period}')

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

    def get_posts_by_date(self, start_date, end_date):
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        start_date = dt.datetime.timestamp(start_date)
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = dt.datetime.timestamp(end_date)

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
        self.posts_per_period = len(self.posts)
        return self.posts

    def get_report(self):
        forbidden_symbols = '|+=[]:*?;«,./\<>~@#$%^-_(){}'
        output = {}
        if self.posts_per_period != 0 or self.posts is None:
            print('Готовлю отчёт...')
            post = self.posts
            post = pd.DataFrame(post)
            trash = ['from_id', 'marked_as_ads', 'edited', 'post_type',
                     'attachments', 'post_source', 'donut', 'short_text_rate',
                     'hash', 'carousel_offset']
            post['owner_id'] = abs(post['owner_id'])
            post['group_link'] = post.apply(lambda x: f'https://vk.com/wall-{self.group_id}_{x["id"]}', axis=1)
            post['date'] = pd.to_datetime(post['date'], unit='s')
            post['likes'] = post.apply(lambda x: x['likes']['count'], axis=1)
            post['comments'] = post.apply(lambda x: x['comments']['count'], axis=1)
            post['reposts'] = post.apply(lambda x: x['reposts']['count'], axis=1)
            try:
                post['views'] = post.apply(lambda x: x['views']['count'], axis=1)
            except TypeError:
                print('TypeError')
            er = (post['likes'] + post['comments'] + post['reposts']) / self.members
            post['ER_post'] = er
            post = post.drop(columns=trash, axis=1)
            post.sort_values(by=['id'])
            post['ER_post'] = post['ER_post'].map('{:.2%}'.format)
            filename = f'{self.name.strip(forbidden_symbols).replace(" ", "_")}_posts_{TIME_NOW}.xlsx'
            try:
                post.to_excel(f'app/output/{filename}', header=True, index=False)
            except OSError:
                filename = f'{self.screen_name}_posts_{TIME_NOW}.xlsx'
                post.to_excel(f'app/output/{filename}', header=True, index=False)
            print('Отчёт готов\n')
            return filename
        else:
            return 'Кэш постов пуст\n'

    def get_members(self):
        print('Начинаю парсинг подписчиков. Это может занять пару минут...')
        offset = 0
        count = 1
        members = []

        while offset < count:
            try:
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
            except KeyError:
                time.sleep(0.5)
        print(f'Парсинг окончен. Собрано {len(members)} подписчиков')
        #members = pd.DataFrame(members, columns=[f'{self.screen_name}_members_id'])
        #df.to_csv(f'./{self.screen_name}_members.csv', header=True, index=False)
        return members

    def get_id(screen_name=str):
        response = rq.get('https://api.vk.com/method/utils.resolveScreenName',
                          params={
                              'access_token': TOKEN,
                              'v': VERSION,
                              'screen_name': screen_name
                          }).json()['response']
        if response:
            return response['object_id']
        return -1
