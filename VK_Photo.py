import requests
from datetime import datetime
from tqdm import tqdm


class VkUserPhoto:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }
        self.res = []

    def get_photo(self, user_id, number):
        """Функция возвращает список из словарей для
                каждой фотографии {'date':, 'likes':, 'url':}"""
        photo_url = self.URL + 'photos.get'
        params_photo = {
            'owner_id': user_id,
            'extended': 1,
            'album_id': 'profile',
            'photo_sizes': 1,
            'count': number
        }
        req = requests.get(photo_url, params={**self.params, **params_photo}).json()
        photo = {}
        for item in tqdm(req['response']['items'], desc='Photo selection', leave=True, ncols=90, unit=' photo'):
            for key in item.keys():
                if key == 'date':
                    photo['date'] = datetime.utcfromtimestamp(item[key]).strftime('%d.%m.%Y')
                elif key == 'likes':
                    photo['likes'] = item[key]['count']
                elif key == 'sizes':
                    photo['size'] = item[key][max_photo(item[key])]['type']
                    photo['url'] = item[key][max_photo(item[key])]['url']
            self.res.append(photo)
            photo = {}
        return self.res


def max_photo(s):
    """Функция возвращает индекс
    фотографии с макс. разрешением"""
    res = []
    for i in s:
        res.append(i['width'] + i['height'])
    return res.index(max(res))