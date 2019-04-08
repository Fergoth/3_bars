import json
import sys


def load_data(filepath):
    with open(filepath) as f:
        json_string = f.read()
        return json.loads(json_string)


def pretty_print_json(json_data):
    print(json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    path = sys.argv[1]
    ugly_json = load_data(path)
    pretty_print_json(ugly_json)