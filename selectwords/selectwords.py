# -*- coding: utf-8 -*-
import argparse
from re import fullmatch
import itertools
import numpy as np


def load_jisho(file: str, row_len: int = -1) -> list:
    fopen = open(file)
    words = fopen.read().splitlines()

    if row_len <= 0:
        return words

    words_filtered = []
    for word in words:
        if len(word) == row_len:
            words_filtered.append(word)
    return words_filtered


def load_problem(file: str) -> list:
    fopen = open(file)
    words = fopen.read().splitlines()

    return words


def is_valid_selectwords(problem: list) -> bool:
    row_len = len(problem[0])
    for row in problem:
        if len(row) != row_len:
            return False
    return True


def get_candidates(jisho: list, problem: list) -> list:
    cands = []
    row_len = len(problem[0])
    col_len = len(problem)

    pattern = ''
    for row in range(row_len):
        characters = ''
        for column in range(col_len):
            characters += problem[column][row]
        pattern = pattern + '[' + characters + ']'

    for word in jisho:
        if fullmatch(pattern, word):
            cands.append(word)

    return cands


def solve(jisho: list, problem: list) -> list:
    problem = sort_selectwords(problem)
    cands = get_candidates(jisho, problem)

    print("候補が{}個あります".format(len(cands)))
    for i, cand in enumerate(cands):
        print("{}. {}".format(i+1, cand))
    print("")

    if len(cands) < len(problem):
        print("候補が少なすぎます")
        return []

    ans = []
    for combination in itertools.combinations(range(len(cands)), len(problem)):
        board = []
        for i in combination:
            board.append(cands[i])
        if sort_selectwords(board) == problem:
            ans.append(board)

    return ans


def sort_selectwords(selectwords: list):
    new_list = []
    for row in selectwords:
        new_list.append(list(row))
    return np.sort(new_list, axis=0).tolist()


def show_selectwords(selectwords: list) -> None:
    row_len = len(selectwords[0])
    for _ in range(row_len):
        print("━", end='')
    print("")
    for row in selectwords:
        print(row)
    for _ in range(row_len):
        print("━", end='')
    print("")


def main():
    parser = argparse.ArgumentParser(description='セレクトワーズのソルバー')
    parser.add_argument('jisho', type=str,
                        help='言葉を並べたファイル（例：豚辞書）')
    parser.add_argument('problem', type=str,
                        help='解きたい問題を書いたテキストファイル')

    args = parser.parse_args()

    problem = load_problem(args.problem)
    if not is_valid_selectwords(problem):
        print("間違った問題です")
        return

    print("問題")
    show_selectwords(problem)
    print("")

    jisho = load_jisho(args.jisho, len(problem[0]))
    answer_list = solve(jisho, problem)

    if len(answer_list) == 0:
        print("解がありません。。。")
        return
    if len(answer_list) == 1:
        print("唯一解です！")
    else:
        print("解が{}個あります。。。".format(len(answer_list)))

    print("")
    print("解答")
    for ans in answer_list:
        show_selectwords(ans)


if __name__ == '__main__':
    main()
