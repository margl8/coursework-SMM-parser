#!/usr/bin/python3
# -*- coding: utf-8 -*-

import utility as ut
import datetime as dt
from dateutil.relativedelta import relativedelta
import time
import pandas as pd


class Group:
    group_id: int
    screen_name: str
    name: str
    members_count: int | str
    members: list

    def __init__(self, group_id: int):
        self.group_id = group_id
        response = ut.vk_send_request(method_name='groups.getById', add_params={
            'group_id': self.group_id,
            'fields': 'members_count'
        })
        response = response[0]
        self.screen_name = response['screen_name']
        self.name = response['name']
        if 'members_count' in response:
            self.members_count = response['members_count']
        else:
            self.members_count = 'no access to members'
        self.members = []

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'ID: {self.group_id}\n'\
               f'Short adress: {self.screen_name}\n' \
               f'Members count: {self.members_count}'

    def __repr__(self):
        return (f'"group_id": {self.group_id}, '
                f'"name": "{self.name}", '
                f'"screen_name": "{self.screen_name}", '
                f'"members_count": {self.members_count}')

    def __call__(self, *args, **kwargs):
        return self.group_id

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    @staticmethod
    def get_id(screen_name: str):
        group_id = ut.vk_send_request(method_name='utils.resolveScreenName', add_params={
            'screen_name': screen_name
        })
        return group_id['object_id']

    def get_members(self, get_all: bool = True, count: int = 1000, offset: int = 0) -> list | str:
        if self.members_count is str:
            return self.members_count
        elif get_all:
            while self.members_count != len(self.members):
                try:
                    ids = ut.vk_send_request(method_name='groups.getMembers',
                                             add_params={'group_id': self.group_id,
                                                         'offset': offset,
                                                         'count': count
                                                         })['items']
                    offset += count
                    self.members.extend(ids)
                except KeyError:
                    time.sleep(0.5)
        return self.members


class Wall:
    owner_id: int


    def __init__(self, group_id: Group | int):
        self.owner_id = group_id

    def __call__(self, *args, **kwargs):
        return self.owner_id

    def get_posts_by_amount(self: Group | int, count: int = 20, offset: int = 0):
        posts = []
        while count != len(posts):
            posts = ut.vk_send_request('wall.get', {'owner_id': -self.owner_id,
                                                    'count': count,
                                                    'offset': offset
                                                    })['items']
        return ut.formalize(posts, self.owner_id)

    def get_posts_by_date(self):
        count = 100
        offset = 0
        #получи сегодняшнюю дату
        today = dt.datetime.today()
        print(today)
        #получи переменную МЕСЯЦ: от сегодняшней даты год и месяц
        #вычти из МЕСЯЦА 12 месяцев
        target_date = today - relativedelta(months=12, days=(today.day - 1))
        print('td', target_date)
        #переведи полученную ДАТА в таймстамп
        target_date = dt.datetime.timestamp(target_date)
        print('td ts', target_date, type(target_date))
        #введи переменную МИНИМАЛЬНАЯ ДАТА
        min_date = target_date + 1
        print(min_date)
        y = []
        counter = 0
        #начни цикл: ПОКА МИНИМАЛЬНАЯ ДАТА не будет больше или равна ДАТЕ
        while min_date > target_date:
            print('iter: ', counter)
            #направь wall.get запрос
            try:
                posts = ut.vk_send_request('wall.get', {'owner_id': -self.owner_id,
                                                        'count': count,
                                                        'offset': offset
                                                        })['items']
                #получи спискок таймстампов постов
                timestamps = [post['date'] for post in posts if not ('is_pinned' in post)]
                print(timestamps)
                #найди наименьшую дату в списке и присвой это значение МИНИМАЛЬНОЙ ДАТЕ
                min_date = min(timestamps)
                print('md', min_date, dt.datetime.fromtimestamp(min_date))
                y.extend(posts)
                offset += count
                print('offset:', offset)
            except KeyError:
                time.sleep(0.5)
        x = [post for post in y if post['date'] > target_date]

        return ut.formalize(x, self.owner_id)
