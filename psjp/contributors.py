# -*- coding: utf-8 -*-
import argparse
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

    return author, puzzle, int(count)


def get_active_authors():
    authors = []
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
            print("{}({}): {}".format(author, a, count))
    return authors


def get_active_puzzles():
    puzzles = []
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
            print("{}({}): {}".format(puzzle, p, count))

    puzzles += [-1]
    return puzzles


def loop(author_id: int = None, puzzle_id: int = None):
    authors = [author_id] if author_id is not None else get_active_authors()
    puzzles = [puzzle_id] if puzzle_id is not None else get_active_puzzles()

    for a in authors:
        for p in puzzles:
            author, puzzle, count = get_psjp_data(a, p)
            if count > 0:
                print("{}({}) {}({}): {}".format(author, a, puzzle, p, count))
            sleep(2)

    return None


def main():
    parser = argparse.ArgumentParser(description='Puzzle Square JPから投稿数などを得る')
    parser.add_argument('--author_id', '-a', type=int,
                        help='作者ID')
    parser.add_argument('--puzzle_id', '-p', type=int,
                        help='パズルID')

    args = parser.parse_args()

    loop(author_id=args.author_id, puzzle_id=args.puzzle_id)


if __name__ == '__main__':
    main()
