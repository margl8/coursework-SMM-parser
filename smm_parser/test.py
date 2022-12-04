import vk_api
from const import TOKEN

tools = vk_api.VkTools(TOKEN)

wall = tools.get_all('wall.get', 100, {'owner_id': -1})
print('Posts count:', wall['count'])
if wall['count']:
    print('First post:', wall['items'][0], '\n')
if wall['count'] > 1:
    print('Last post:', wall['items'][-1])
