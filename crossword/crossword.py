# -*- coding: utf-8 -*-
import argparse


def load_file(file: str) -> str:
    fopen = open(file)
    input_lines = fopen.read().splitlines()

    return input_lines


def cut_line(lines: list) -> dict:
    num = 1
    words = {}
    for line in lines:
        word = ""
        for chara in line:
            if chara in  ('＠', '@', '＃', '#'):
                if len(word) > 1:
                    words[num] = word
                    num += 1
                word = ''
            else:
                word += chara
        if len(word) > 1:
            words[num] = word
            num += 1

    return words


def transposition_list(lines: list) -> list:
    tr_dict = {}
    for row, line in enumerate(lines):
        for column, chara in enumerate(line):
            if row == 0:
                tr_dict[column] = chara
            else:
                tr_dict[column] += chara

    return tr_dict.values()


def load_problem(file: str) -> dict:
    board = load_file(file)

    problem = {}
    problem["board"] = board

    row_words = cut_line(board)
    problem["row"] = row_words

    column_words = cut_line(transposition_list(board))
    problem["column"] = column_words

    return problem


def show_problem(problem: dict) -> None:
    print("クロスワード")
    print()

    for line in problem["board"]:
        print(line)
    print()

    keys = {"row": "↓ヨコのカギ", "column": "↓タテのカギ"}
    for key, str_key in keys.items():
        print(str_key)
        for num, word in problem[key].items():
            print("{} {}".format(num, word))
        print()


def check_words(problem: dict) -> None:
    print("チェック")


def main():
    parser = argparse.ArgumentParser(description='クロスワードの盤面から言葉を抜き出します')
    parser.add_argument('file', type=str,
                        help='クロスワードの盤面')
    parser.add_argument('--check', '-c', action='store_true',
                        help='言葉の重複などを調べます')

    args = parser.parse_args()

    problem = load_problem(args.file)

    if args.check:
        check_words(problem)
    else:
        show_problem(problem)


if __name__ == '__main__':
    main()
