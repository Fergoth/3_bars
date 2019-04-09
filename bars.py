import json
import sys
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    try:
        with open(filepath, encoding='utf-8') as file:
            data_from_file = json.load(file)
            return data_from_file['features']
    except FileNotFoundError:
        print('Файл не найден')
    except json.decoder.JSONDecodeError:
        print('Файл содержит данные не в формате json')

def get_biggest_bar(bars):
    biggest_bar = max(bars, key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = min(bars, key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return smallest_bar


def get_closest_bar(bars, longitude, latitude):
    closest_bar = min(bars, key=lambda x: get_distance(longitude, latitude, *x['geometry']['coordinates']))
    return closest_bar


# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def get_distance(lon1, lat1, lon2, lat2):
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


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        print('Требуется путь к файлу как аргумент')
        sys.exit(0)
    json_data = load_data(path)
    if json_data:
        while 1:
            print('Введите текущие координаты через пробел')
            try:
                lon, lat = map(float, input().split())
            except ValueError:
                print('Введите два числа в формате float через пробел \n Например 37.454 32.4353')
            else:
                break
        print('Ближайший бар:')
        print_bar(get_closest_bar(json_data, lon, lat))
        print('Самый большой бар:')
        print_bar(get_biggest_bar(json_data))
        print('Самый маленький бар:')
        print_bar(get_smallest_bar(json_data))
