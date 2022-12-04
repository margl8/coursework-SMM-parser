from classes import VkGroup

if __name__ == '__main__':
    id = 22564985
    group = VkGroup()  # происходит __init__
    group(id)  # происходит __call__, который принимает ID
    print(group)
    print(repr(group))
    print(group.get_posts_by_date('01-06-2022', '30-06-2022'))
    group.get_report()
