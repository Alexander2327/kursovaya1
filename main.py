from YA_Photo import *

with open('vk_token.txt', 'r') as file:
    token_vk = file.read().strip()

with open('ya_token.txt', 'r') as file:
    token_ya = file.read().strip()

version = '5.131'

if __name__ == '__main__':
    while True:
        ID = input('Введите id пользователя vk: ')
        num = input('Введите количество фотографий для сохранения на ЯндексДиск: ')
        if num.isdigit() is False:
            num = 5
        y = YandexPhoto(token_ya)
        y.upload(user_id=ID, number=num, token=token_vk, version=version)
        if input(
                'Фотографии загружены на Диск, файл с результатами создан! Продолжить выполнение программы?(Y/N) ').lower() == 'n':
            break