# -*- coding: utf-8 -*-
import argparse
from re import fullmatch
import itertools
from numpy import sort


def load_jisho(file: str, width: int = -1) -> list:
    fopen = open(file)
    words = fopen.read().splitlines()

    if width <= 0:
        return words

    words_filtered = []
    for word in words:
        if len(word) == width:
            words_filtered.append(word)
    return words_filtered


def load_problem(file: str) -> list:
    fopen = open(file)
    problem = fopen.read().splitlines()

    def _is_valid() -> bool:
        if len(problem) < 2 or len(problem[0]) < 2:
            return False
        width = len(problem[0])
        for row in problem:
            if len(row) != width:
                return False
        return True

    return problem if _is_valid() else []


def get_candidates(jisho: list, problem: list) -> list:
    candidates = []
    width = len(problem[0])
    height = len(problem)

    pattern = ''
    for row in range(width):
        characters = ''
        for column in range(height):
            characters += problem[column][row]
        pattern = pattern + '[' + characters + ']'

    for word in jisho:
        if fullmatch(pattern, word):
            candidates.append(word)

    return candidates


def solve(jisho: list, problem: list) -> list:
    sorted_problem = sort_selectwords(problem)
    candidates = get_candidates(jisho, problem)

    height = len(problem)
    num_cand = len(candidates)

    print("候補が{}個あります".format(num_cand))
    for i in range(num_cand):
        print("{}. {}".format(i+1, candidates[i]))
    print("")

    if num_cand < height:
        print("候補が少なすぎます")
        return []

    ans = []
    for combination in itertools.combinations(range(num_cand), height):
        board = [candidates[i] for i in combination]
        if sort_selectwords(board) == sorted_problem:
            ans.append(board)

    return ans


def sort_selectwords(selectwords: list):
    listed = [list(i) for i in selectwords]
    return sort(listed, axis=0).tolist()


def show_selectwords(selectwords: list) -> None:
    width = len(selectwords[0])
    for _ in range(width):
        print("━", end='')
    print("")
    for row in selectwords:
        print(row)
    for _ in range(width):
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
    if len(problem) == 0:
        print("問題が間違っています")
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
