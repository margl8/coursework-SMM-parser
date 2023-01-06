from app.vk import Group, Wall
import pandas as pd
from const import TIME_NOW
#145456773 welltex_perm
#22564985 welltex
#25240087 hikk
#38489 poli
y = Wall(25240087)
print(y)
z = y.get_posts_by_date()

pd.DataFrame(z).to_excel(f'./filename_{TIME_NOW}.xlsx', header=True, index=False)
