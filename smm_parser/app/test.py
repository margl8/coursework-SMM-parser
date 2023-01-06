#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests as rq

TOKEN = 'fcf784d2fcf784d2fcf784d206ffe7472fffcf7fcf784d29fdf12d1cff39e144bbbaa42'
VERSION = 5.131


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

def clean_link(link=str):
    link = link.strip()
    link = link.split('/')
    return link.pop()


def decorator_function(func):
    def wrapper(*args, **kwargs):
        print('Функция-обёртка!')
        print('Оборачиваемая функция: {}'.format(func))
        print('Выполняем обёрнутую функцию...')
        func()
        print('Выходим из обёртки')
    return wrapper


@decorator_function
def hello_world():
        print('Hello world!')
hello_world()