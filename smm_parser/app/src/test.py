#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import time
from classes import VkGroup

if __name__ == '__main__':
    group = VkGroup()
    df = pd.read_csv('db/screen_names.csv', header=0)
    groups_report = pd.DataFrame()
    lst = []
    rep = pd.DataFrame(group.__dict__)
    def request(id):
        # программа получает ID группы
        group(id)
        # собирает посты за ноябрь
        group.get_posts_by_date('01-11-2022', '30-11-2022')
        print(group)
        group.get_report()

    for index, row in df.iterrows():

        try:
            request(VkGroup.get_id(row['screen_name']))
        except TypeError:
            time.sleep(0.5)
            request(VkGroup.get_id(row['screen_name']))
        except KeyError:
            time.sleep(0.5)
            request(VkGroup.get_id(row['screen_name']))
        finally:
            rep.loc[len(rep)] = group.__dict__
    rep.drop(columns=['posts'], axis=1)
    rep.to_excel(f'./!ALL_GROUPS_REPORT.xlsx',
                 header=True, index=False)
