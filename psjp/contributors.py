# -*- coding: utf-8 -*-
import argparse
import re
import requests
from time import sleep


PSJP_URL = 'https://puzsq.jp/main/index.php'

MAX_AUTHOR_ID = 1000
MAX_PUZZLE_ID = 1000

SEARCH_AUTHOR = r'(?<=作：)\w+'
SEARCH_PUZZLE = r'(?<=種類：)\w+'
SEARCH_COUNT = r'(?<=取得件数：)[0-9]+'


def get_psjp_data(author_id: int, puzzle_id: int) -> (str, str, int):
    url = "{}?puzzle={}&author={}".format(PSJP_URL, puzzle_id, author_id)
    r = requests.get(url)

    author_re = re.search(SEARCH_AUTHOR, r.text)
    if author_re is None:
        return None, None, 0
    author = author_re.group(0)

    puzzle_re = re.search(SEARCH_PUZZLE, r.text)
    if puzzle_re is None:
        return None, None, 0
    puzzle = puzzle_re.group(0)

    count = re.search(SEARCH_COUNT, r.text).group(0)

    return author, puzzle, int(count)


def loop(author_id: int = None, puzzle_id: int = None):
    author_range = range(1, MAX_AUTHOR_ID) if author_id is None else range(author_id, author_id + 1)
    puzzle_range = range(1, MAX_PUZZLE_ID) if puzzle_id is None else range(puzzle_id, puzzle_id + 1)

    for a in author_range:
        for p in puzzle_range:
            author, puzzle, count = get_psjp_data(a, p)
            if author is not None:
                print("{} {} {}".format(author, puzzle, count))
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
