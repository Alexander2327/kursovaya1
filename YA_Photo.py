from VK_Photo import *
import json


class YandexPhoto:
    URL = 'https://cloud-api.yandex.net/'
    user = None

    def __init__(self, token):
        self.token = token

    def upload(self, user_id, number, token, version):
        """Функция загрузки фотографий на Яндекс Диск"""
        upload_url = self.URL + 'v1/disk/resources/upload'
        self.user = VkUserPhoto(token, version)
        create_folder(f'ID_{user_id}', self.token)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        inf = []
        list_likes = []
        list_photo = self.user.get_photo(user_id, number)
        for user_photo in tqdm(list_photo, desc='Uploading to YaDisk', unit=' photo', leave=True, ncols=90):
            for likes in list_photo:
                list_likes.append(likes['likes'])
            list_likes.remove(user_photo['likes'])
            if user_photo['likes'] in list_likes:
                photo_name = f'{user_photo["likes"]}({user_photo["date"]})'
            else:
                photo_name = f'{user_photo["likes"]}'
            list_likes = []
            params = {
                'url': user_photo['url'],
                'path': f'ID_{user_id}/{photo_name}.jpg'
            }
            req = requests.post(upload_url, headers=headers, params=params)
            req.raise_for_status()
            inf.append({
                'file_name': f'{photo_name}.jpg',
                'size': user_photo['size']
            })
        create_json(user_id, inf)


def create_folder(folder_name, token):
    """Функция создания папки на Яндекс Диске"""
    folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {token}'
    }
    params = {'path': folder_name}
    req = requests.put(folder_url, headers=headers, params=params)
    req.raise_for_status()


def create_json(user_id, inf):
    """Функция создает Json файл с результатами по загрузке"""
    j = json.dumps(inf)
    with open(f'json_file(ID_{user_id}).json', 'w', encoding='utf-8') as f:
        f.write(j)