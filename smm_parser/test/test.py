import pandas as pd
import time
from app.src.vk_group import VkGroup

if __name__ == '__main__':
    group = VkGroup()
    df = pd.read_csv('app/db/screen_names.csv', header=0)
    groups_report = pd.DataFrame()
    lst = []
    rep = pd.DataFrame(group.__dict__)
    def request(id):
        # программа получает ID группы
        group(id)
        # собирает посты за ноябрь
        group.get_posts_by_date('2022-11-01', '2022-11-30')
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
    rep = rep.drop(columns=['posts'], axis=1)
    rep.to_excel(f'app/output/!ALL_GROUPS_REPORT.xlsx',
                 header=True, index=False)
