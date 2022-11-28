from classes import VkGroup

if __name__ == '__main__':
    id = 22564985
    group = VkGroup()  # происходит __init__
    group(id)  # происходит __call__, который принимает ID
    print(group)
    print(repr(group))
    group.get_posts(10)  # получить статистику последних 10 постов
    group.get_report()  # получить exl-отчёт по последним 10 постам