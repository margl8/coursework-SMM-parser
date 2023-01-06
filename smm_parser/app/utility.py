import requests as rq
import pandas as pd
import datetime as dt
import time
from const import TOKEN, VERSION


def clear_link(link: str):
    link = link.strip()
    link = link.split('/')
    return link[-1::]


def vk_send_request(method_name: str, add_params: dict):
    response = rq.get(url=f"https://api.vk.com/method/{method_name}",
                      params={
                                 'access_token': TOKEN,
                                 'v': VERSION
                             } | add_params).json()
    return response['response']


def formalize(posts, id):
    y = []
    for i in posts:
        x = {'link': f"https://vk.com/wall-{id}_{i['id']}",
             'date': dt.datetime.fromtimestamp(i['date']),  # '7': i['text'],
             'likes': i['likes']['count'], 'comments': i['comments']['count'],
             'reposts': i['reposts']['count'], 'views': i['views']['count']}
        y.append(x)
    return y
