#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.src.vk_group import VkGroup

#"%d-%m-%Y"

if __name__ == '__main__':
    id = 22564985
    group = VkGroup()  # происходит __init__
    group(id)  # происходит __call__, который принимает ID
    print(group)
    group.get_members()




