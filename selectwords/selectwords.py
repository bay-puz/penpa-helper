# -*- coding: utf-8 -*-
import argparse
from re import fullmatch
import itertools


GRAY = '🔲'


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
    input_problem = fopen.read().splitlines()

    problem = [word.replace('#', GRAY).replace('＃', GRAY) for word in input_problem]

    def _is_valid() -> bool:
        if len(problem) < 2 or len(problem[0]) < 2:
            return False
        width = len(problem[0])
        for row in problem:
            if len(row) != width:
                return False
        return True

    return problem if _is_valid() else []


def find_candidates(jisho: list, problem: list) -> list:
    patterns = generate_patterns(problem)

    candidates = []
    for word in jisho:
        for pattern, pos_gray in patterns:
            if fullmatch(pattern, word):
                gray_char = word[pos_gray] if pos_gray >= 0 else None
                candidates.append((word, gray_char))
                break

    return candidates


def generate_patterns(problem: list) -> list:
    width = len(problem[0])
    height = len(problem)

    count_gray = [0 for _ in range(width)]
    pattern_char = [None for _ in range(width)]
    for row in range(width):
        characters = ''
        for column in range(height):
            if problem[column][row] == GRAY:
                count_gray[row] += 1
            else:
                characters += problem[column][row]
        if characters != '':
            pattern_char[row] = '[' + characters + ']'

    def _check_pattern(pattern_set: list) -> bool:
        for row in range(width):
            if pattern_set[row]:
                if not pattern_char[row]:
                    return False
            else:
                if count_gray[row] == 0:
                    return False
        return True

    patterns = []
    for pattern_set in itertools.product([True, False], repeat=width):
        if not _check_pattern(pattern_set):
            continue

        pattern = ''
        pos_gray = -1
        for row in range(width):
            if pattern_set[row]:
                pattern += pattern_char[row]
            else:
                if pos_gray == -1:
                    pattern += '(.)'
                    pos_gray = row
                else:
                    pattern += r'\1'
        patterns.append((pattern, pos_gray))

    return patterns


def solve(jisho: list, problem: list) -> list:
    candidates = find_candidates(jisho, problem)

    height = len(problem)
    width = len(problem[0])
    num_cand = len(candidates)

    print("候補が{}個あります".format(num_cand))
    for i in range(num_cand):
        print("{}. {}".format(i + 1, candidates[i][0]))
    print("")

    if num_cand < height:
        print("候補が少なすぎます")
        return []

    def _check_gray(combination) -> bool:
        gray_char = None
        for pos in combination:
            if candidates[pos][1] is not None:
                if gray_char is None:
                    gray_char = candidates[pos][1]
                elif candidates[pos][1] != gray_char:
                    return False
        return True

    def _get_gray_char(combination) -> str:
        for pos in combination:
            if candidates[pos][1] is not None:
                return candidates[pos][1]
        return None

    def _compare_problem(board: list, gray_char: str) -> bool:
        for row in range(width):
            board_slice = []
            problem_slice = []
            for column in range(height):
                board_slice.append(board[column][row])
                if problem[column][row] == GRAY and gray_char is not None:
                    problem_slice.append(gray_char)
                else:
                    problem_slice.append(problem[column][row])
            if sorted(board_slice) != sorted(problem_slice):
                return False
        return True

    answers = []
    for combination in itertools.combinations(range(num_cand), height):
        if not _check_gray(combination):
            continue

        board = [candidates[i][0] for i in combination]
        gray_char = _get_gray_char(combination)
        if _compare_problem(board, gray_char):
            answers.append(board)

    return answers


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
