# -*- coding: utf-8 -*-
import argparse
import json
import re
import requests
from time import sleep


PSJP_URL = 'https://puzsq.jp/main/index.php'

SEARCH_AUTHOR = r'(?<=作：)[^<]+'
SEARCH_PUZZLE = r'(?<=種類：)[^<]+'
SEARCH_COUNT = r'(?<=取得件数：)[0-9]+'


def get_psjp_data(author_id: int, puzzle_id: int) -> (str, str, int):
    url = "{}?puzzle={}&author={}".format(PSJP_URL, puzzle_id, author_id)
    r = requests.get(url)

    author_re = re.search(SEARCH_AUTHOR, r.text)
    author = author_re.group(0) if author_re is not None else None

    puzzle_re = re.search(SEARCH_PUZZLE, r.text)
    puzzle = puzzle_re.group(0) if puzzle_re is not None else None

    count = re.search(SEARCH_COUNT, r.text).group(0)

    if author_id == 0:
        author = "ALL"
    if puzzle_id == 0:
        puzzle = "ALL"
    return author, puzzle, int(count)


def get_active_authors():
    authors = [0]
    a = 0
    while True:
        a += 1
        if 1 < a and a < 23:
            continue

        author, puzzle, count = get_psjp_data(a, 0)
        if author is None:
            break
        if count > 0:
            authors += [a]
    return authors


def get_active_puzzles():
    puzzles = [-1, 0]
    p = 0
    while True:
        p += 1
        if p == 23 or p == 24 or p == 60 or p == 93:
            continue

        author, puzzle, count = get_psjp_data(0, p)
        if puzzle is None:
            break
        if count > 0:
            puzzles += [p]

    return puzzles


def loop(author_id: int = None, puzzle_id: int = None):
    authors = [author_id] if author_id is not None else get_active_authors()
    puzzles = [puzzle_id] if puzzle_id is not None else get_active_puzzles()

    data = []
    for a in authors:
        for p in puzzles:
            author, puzzle, count = get_psjp_data(a, p)
            d = {"author": {"id": a, "name": author}, "puzzle": {"id": p, "name": puzzle}, "count": count}
            data += [d]
            sleep(2)

    return data


def main():
    parser = argparse.ArgumentParser(description='Puzzle Square JPから投稿数などを得る')
    parser.add_argument('--author_id', '-a', type=int,
                        help='作者ID')
    parser.add_argument('--puzzle_id', '-p', type=int,
                        help='パズルID')

    args = parser.parse_args()

    psjp_data = loop(author_id=args.author_id, puzzle_id=args.puzzle_id)
    print(json.dumps(psjp_data))


if __name__ == '__main__':
    main()
