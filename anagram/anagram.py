# -*- coding: utf-8 -*-
import argparse
import itertools


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


def solve(jisho: list, problem: str, additional: int) -> list:
    width = len(problem) - additional
    candidates = []
    answers = []
    for permutation in itertools.permutations(range(len(problem)), width):
        candidate = ''
        for pos in permutation:
            candidate += problem[pos]
        if candidate not in candidates:
            if candidate in jisho:
                answers.append(candidate)
            candidates.append(candidate)

    return answers


def main():
    parser = argparse.ArgumentParser(description='アナグラム・チマタグラムのソルバー')
    parser.add_argument('jisho', type=str,
                        help='言葉を並べたファイル（例：豚辞書）')
    parser.add_argument('problem', type=str, help='問題')
    parser.add_argument('-n', type=int, default=0, help='加えた文字数（チマタグラムなら1）')

    args = parser.parse_args()

    problem = normalize(args.problem)
    if args.n == 0:
        print("アナグラム")
    elif args.n == 1:
        print("チマタグラム")
    else:
        print("チマタグラム（加えた文字数={}）".format(args.n))
    print("問題：{} ".format(problem))
    jisho = load_jisho(args.jisho, len(problem) - args.n)
    answer_list = solve(jisho, problem, args.n)

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
