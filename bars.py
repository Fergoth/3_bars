import json
import sys
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    with open(filepath, encoding='utf-8') as f:
        json_str = json.load(f)
        return json_str['features']


def get_biggest_bar(data):
    biggest_bar = max(data, key=lambda x: x['properties']['Attributes']["SeatsCount"])
    print('Самый большой бар')
    pretty_print_json(biggest_bar)


def get_smallest_bar(data):
    smallest_bar = min(data, key=lambda x: x['properties']['Attributes']["SeatsCount"])
    print('Самый маленький бар:')
    pretty_print_json(smallest_bar)


def get_closest_bar(data, longitude, latitude):
    closest_bar = min(data, key=lambda x: haversine(longitude, latitude, *x['geometry']['coordinates']))
    print('Ближайший бар:')
    pretty_print_json(closest_bar)


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def pretty_print_json(json_data):
    bar_address = json_data['properties']['Attributes']['Address']
    bar_name = json_data['properties']['Attributes']['Name']
    print('Название бара: {} \nАдрес: {}\n'.format(bar_name, bar_address))


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        path = 'bars.json'
    json_data = load_data(path)
    print('Введите текущие координаты через пробел')
    lon, lat = map(float, input().split())
    get_closest_bar(json_data, lon, lat)
    get_biggest_bar(json_data)
    get_smallest_bar(json_data)
