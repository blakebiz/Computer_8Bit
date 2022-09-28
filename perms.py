import json


def get_permutations(n):
    with open(f'permutations_{n}.json') as f:
        return json.load(f)

