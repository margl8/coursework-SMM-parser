import requests as rq
import pandas as pd
import openpyxl
from const import TOKEN, TIME_NOW, VERSION


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
        return(f'id={self.group_id}, '
               f'screen_name="{self.screen_name}", '
               f'members ={self.members}')

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

    def get_report(self):
        print('Готовлю отчёт...')
        post = self.posts
        post = pd.DataFrame(post)
        post = post.drop(columns=['from_id', 'owner_id', 'marked_as_ads',
                                  'edited', 'post_type', 'attachments',
                                  'post_source', 'donut', 'short_text_rate',
                                  'hash'], axis=1)
        post.insert(1, 'link', "NaN")
        post['link'] = post.apply(lambda x: f'https://vk.com/wall-{self.group_id}_{x["id"]}', axis=1)
        post['date'] = pd.to_datetime(post['date'], unit='s')
        post['comments'] = post.apply(lambda x: x['comments']['count'], axis=1)
        post['reposts'] = post.apply(lambda x: x['reposts']['count'], axis=1)
        post['likes'] = post.apply(lambda x: x['likes']['count'], axis=1)
        post['views'] = post.apply(lambda x: x['views']['count'], axis=1)

        print('Отчёт готов')
        post.to_excel(f'./{self.name}_posts_{TIME_NOW}.xlsx', header=True, index=False)

    def get_posts(self, count):
        # count = int(input('Сколько постов нужно получить?'))
        #  offset = int(input('offset'))
        request = rq.get("https://api.vk.com/method/wall.get",
                         params={
                             'access_token': TOKEN,
                             'v': VERSION,
                             'owner_id': -self.group_id,
                             'count': count,
                             'offset': 0
                         }).json()['response']['items']
        self.posts = request
        print('Посты собраны')
        return pd.DataFrame(self.posts)
