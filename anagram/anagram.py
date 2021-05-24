# -*- coding: utf-8 -*-
import argparse
from re import fullmatch


def load_jisho(file: str, width: int) -> list:
    fopen = open(file)
    words = fopen.read().splitlines()

    words_filtered = []
    for word in words:
        if len(word) == width:
            words_filtered.append(word)
    return words_filtered


def normalize(problem: str) -> str:
    str_before = "ぁぃぅぇぉゃゅょっ"
    str_after = "あいうえおやゆよつ"
    normalized = ''
    for chara in problem:
        if chara in str_before:
            normalized += str_after[str_before.index(chara)]
        else:
            normalized += chara
    return normalized


def generate_pattern(problem: str, len_answer: int) -> str:
    chars = set(problem)
    char_pattern = '[' + str.join('', chars) + ']'

    pattern = ''
    for _ in range(len_answer):
        pattern += char_pattern
    return pattern


def generate_map(problem: str) -> dict:
    char_counts = {}
    for char in problem:
        if char in char_counts:
            continue
        char_counts[char] = problem.count(char)
    return char_counts


def check_word(word: str, pattern: str, char_map: dict):
    if not fullmatch(pattern, word):
        return False

    for char, num in char_map.items():
        if word.count(char) > num:
            return False
    return True


def solve(jisho: list, problem: str, len_answer: int) -> list:
    pattern = generate_pattern(problem, len_answer)
    char_map = generate_map(problem)

    answers = []
    for word in jisho:
        if check_word(word, pattern, char_map):
            answers.append(word)

    return answers


def main():
    parser = argparse.ArgumentParser(description='アナグラム・チマタグラムのソルバー')
    parser.add_argument('jisho', type=str,
                        help='言葉を並べたファイル（例：豚辞書）')
    parser.add_argument('problem', type=str, help='問題')
    parser.add_argument('-n', type=int, default=0, help='加えた文字数（チマタグラムなら1）')

    args = parser.parse_args()

    problem = normalize(args.problem)
    len_answer = len(problem) - args.n
    if args.n == 0:
        print("アナグラム")
    elif args.n == 1:
        print("チマタグラム")
    else:
        print("チマタグラム（加えた文字数={}）".format(args.n))
    print("問題：{} ".format(problem))
    jisho = load_jisho(args.jisho, len_answer)
    answer_list = solve(jisho, problem, len_answer)

    if len(answer_list) == 0:
        print("解がありません。。。")
        return
    if len(answer_list) == 1:
        print("唯一解です！")
    else:
        print("解が{}個あります。。。".format(len(answer_list)))

    print("解答：")
    for answer in answer_list:
        print(answer)


if __name__ == '__main__':
    main()
