# -*- coding: utf-8 -*-
import argparse
import json
import re
import requests
from multiprocessing import Pool
from sys import stderr
from time import sleep


PSJP_URL = 'https://puzsq.jp/main/index.php'

SEARCH_AUTHOR = r'(?<=作：)[^<]+'
SEARCH_PUZZLE = r'(?<=種類：)[^<]+'
SEARCH_COUNT = r'(?<=取得件数：)[0-9]+'

MAX_PROCESSES = 5


def get_psjp_data(author_id: int, puzzle_id: int, use_stdout: bool = True):
    url = "{}?puzzle={}&author={}".format(PSJP_URL, puzzle_id, author_id)
    try:
        sleep(1)
        r = requests.get(url, timeout=30)
    except Exception as e:
        print(e, file=stderr)
        print("url: {}".format(url), file=stderr)
        return (author_id, puzzle_id, -1)

    author_re = re.search(SEARCH_AUTHOR, r.text)
    author = author_re.group(0) if author_re is not None else None

    puzzle_re = re.search(SEARCH_PUZZLE, r.text)
    puzzle = puzzle_re.group(0) if puzzle_re is not None else None

    count_re = re.search(SEARCH_COUNT, r.text)
    count = int(count_re.group(0)) if count_re is not None else 0

    if author_id == 0:
        author = "ALL"
    if puzzle_id == 0:
        puzzle = "ALL"

    data = {"author": {"id": author_id, "name": author}, "puzzle": {"id": puzzle_id, "name": puzzle}, "count": count}

    if use_stdout:
        print(json.dumps(data))
    else:
        print(json.dumps(data), file=stderr)

    return (author, puzzle, count)


def get_active_authors(all: bool = True):
    authors = [0]
    a = 0
    while True:
        a += 1
        if 1 < a and a < 23:
            continue

        author, puzzle, count = get_psjp_data(a, 0, False)
        if count < 0:
            print("cannot get data for author_id={}".format(a), file=stderr)
        if author is None:
            break
        if count > 0 or all:
            authors += [a]

    return authors


def get_active_puzzles(all: bool = True):
    puzzles = [-1, 0]
    p = 0
    while True:
        p += 1
        if p == 23 or p == 24 or p == 60 or p == 93:
            continue

        author, puzzle, count = get_psjp_data(0, p, False)
        if count < 0:
            print("cannot get data for puzzle_id={}".format(p), file=stderr)
        if puzzle is None:
            break
        if count > 0 or all:
            puzzles += [p]

    return puzzles


def loop(author_id: int = None, puzzle_id: int = None, all: bool = False):
    authors = [author_id] if author_id is not None else get_active_authors(all)
    puzzles = [puzzle_id] if puzzle_id is not None else get_active_puzzles(all)

    arg_list = []
    for a in authors:
        for p in puzzles:
            arg_list += [(a, p)]

    map = []
    with Pool(processes=MAX_PROCESSES) as pool:
        map = pool.starmap(get_psjp_data, arg_list)

    for author, puzzle, count in map:
        if count < 0:
            print("retry: p={}, a={}".format(puzzle, author), file=stderr)
            a, p, c = get_psjp_data(author, puzzle)
            if c < 0:
                print("failed to retry: p={}, a={}".format(a, p), file=stderr)

    return True


def main():
    parser = argparse.ArgumentParser(description='Puzzle Square JPから投稿数などを得る')
    parser.add_argument('--author_id', '-a', type=int, help='作者ID')
    parser.add_argument('--puzzle_id', '-p', type=int, help='パズルID')
    parser.add_argument('--show-all', action='store_true', help='問題が0問でも出力する')

    args = parser.parse_args()

    loop(author_id=args.author_id, puzzle_id=args.puzzle_id, all=args.show_all)


if __name__ == '__main__':
    main()
