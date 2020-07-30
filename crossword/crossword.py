# -*- coding: utf-8 -*-
import argparse


def load_file(file: str) -> list:
    fopen = open(file)
    input_lines = fopen.read().splitlines()

    return input_lines


def is_black(chara: str) -> bool:
    return chara in ('@', '＠', '#', '＃')


def is_number(row: int, column: int, board: list) -> bool:
    row_end = len(board[0])
    column_end = len(board)

    def is_whitecell(row: int, column: int) -> bool:
        if row not in range(0, row_end):
            return False
        if column not in range(0, column_end):
            return False

        return not is_black(board[column][row])

    if not is_whitecell(row, column):
        return False

    if not is_whitecell(row-1, column) and is_whitecell(row+1, column):
        return True
    if not is_whitecell(row, column-1) and is_whitecell(row, column+1):
        return True

    return False


def transposition_list(lines: list) -> list:
    tr_dict = {}
    for row, line in enumerate(lines):
        for column, chara in enumerate(line):
            if row == 0:
                tr_dict[column] = chara
            else:
                tr_dict[column] += chara

    return list(tr_dict.values())


def set_keys(lines: str) -> dict:
    lines_tr = transposition_list(lines)

    keys = {}
    keys_tr = {}
    key_id = 1
    for column, line in enumerate(lines_tr):
        for row, _ in enumerate(line):
            if is_number(row, column, lines_tr):
                keys[key_id] = [column, row]
                keys_tr[key_id] = [row, column]
                key_id += 1

    return keys, keys_tr


def set_words(lines: dict, keys: dict) -> dict:
    words = {}
    head = 0
    for line in lines:
        word = ''
        for chara in line:
            if is_black(chara):
                if len(word) > 1:
                    words[head] = word
                head += len(word) + 1
                word = ''
            else:
                word += chara
        if len(word) > 1:
            words[head] = word
        head += len(word)

    row_size = len(lines[0])
    words_key = {}
    for key_id, key_pos in keys.items():
        pos = key_pos[0] + key_pos[1] * row_size
        if pos in words:
            words_key[key_id] = words[pos]

    return words_key


def get_words_keys(lines: list):
    lines_tr = transposition_list(lines)
    keys, keys_tr = set_keys(lines)

    row_words = set_words(lines, keys)
    column_words = set_words(lines_tr, keys_tr)

    return row_words, column_words


def load_problem(file: str) -> dict:
    board = load_file(file)

    problem = {}
    problem["board"] = board

    row_words, column_words = get_words_keys(board)
    problem["row"] = sorted(row_words.items())
    problem["column"] = sorted(column_words.items())

    return problem


def show_problem(problem: dict) -> None:
    print("クロスワード")
    print()

    for line in problem["board"]:
        print(line)
    print()

    keys = {"row": "→ヨコのカギ", "column": "↓タテのカギ"}
    for key, str_key in keys.items():
        print(str_key)
        for num, word in problem[key]:
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
