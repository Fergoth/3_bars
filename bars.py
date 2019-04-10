import json
import sys
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    with open(filepath, encoding='utf-8') as file:
        data_from_file = json.load(file)
        return data_from_file['features']


def get_biggest_bar(bars):
    biggest_bar = max(bars,
                      key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = min(bars, key=lambda x: x['properties']['Attributes'][
        'SeatsCount'])
    return smallest_bar


def get_closest_bar(bars, longitude, latitude):
    closest_bar = min(bars, key=lambda x: get_distance(longitude, latitude,
                                                       *x['geometry'][
                                                           'coordinates']))
    return closest_bar


def get_distance(lon1, lat1, lon2, lat2):
    '''Get distance between two points by haversine formula.
    Description on stackoverflow
    https://stackoverflow.com/a/4913653'''
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def print_bar(bar):
    bar_address = bar['properties']['Attributes']['Address']
    bar_name = bar['properties']['Attributes']['Name']
    print('Название бара: {} \nАдрес: {}\n'.format(bar_name, bar_address))


def input_coord():
    print('Введите текущие координаты через пробел')
    try:
        lon, lat = map(float, input().split())
    except ValueError:
        print(
            'Введите два числа в формате float через пробел \n'
            'Например 37.454 32.4353')
    return lon, lat


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit('Требуется путь к файлу как аргумент')
    try:
        data_from_file = load_data(path)
    except FileNotFoundError:
        sys.exit('Файл не найден')
    except json.decoder.JSONDecodeError:
        sys.exit('Файл содержит данные не в формате json')
    lon, lat = input_coord()
    print('Ближайший бар:')
    print_bar(get_closest_bar(data_from_file, lon, lat))
    print('Самый большой бар:')
    print_bar(get_biggest_bar(data_from_file))
    print('Самый маленький бар:')
    print_bar(get_smallest_bar(data_from_file))
