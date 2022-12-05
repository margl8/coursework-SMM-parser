#!/usr/bin/python3
# -*- coding: utf-8 -*-


from classes import VkGroup

#"%d-%m-%Y"

if __name__ == '__main__':
    id = 22564985
    group = VkGroup()  # происходит __init__
    group(id)  # происходит __call__, который принимает ID
    print(group)
    print(repr(group))
    group.get_members()
    group.get_posts_by_date('01-12-2022', '05-12-2022')

