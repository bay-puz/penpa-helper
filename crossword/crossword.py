# -*- coding: utf-8 -*-
import argparse


BLACKCELL = "＠"
BLANKCELL = "？"


def validate(input_lines: list) -> bool:
    length = len(input_lines[0])
    for line in input_lines:
        if len(line) != length:
            return False

    return True


def normalize(input_str: str) -> str:
    normalize_map = {}

    remove_str = " 　."
    for _, remove in enumerate(remove_str):
        normalize_map[remove] = ""

    small_str = "ァィゥェォヵヶッャュョ"
    large_str = 'アイウエオカケツヤユヨ'
    for num, small in enumerate(small_str):
        normalize_map[small] = large_str[num]

    black_str = "@＠#＃"
    for _, black in enumerate(black_str):
        normalize_map[black] = BLACKCELL

    blank_str = "?？.-"
    for _, blank in enumerate(blank_str):
        normalize_map[blank] = BLANKCELL

    normalize_table = str.maketrans(normalize_map)

    return input_str.translate(normalize_table)


def remove_numeric(input_lines: list) -> list:
    removed_lines = []
    for line in input_lines:
        if not line.isnumeric():
            removed_lines.append(line)

    return removed_lines


def load_file(file: str) -> list:
    fopen = open(file)
    input_str = fopen.read()

    normalized_lines = normalize(input_str).splitlines()
    return remove_numeric(normalized_lines)


def is_black(chara: str) -> bool:
    return chara == BLACKCELL


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


def get_problem(board: list) -> dict:
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
    print("クロスワードのチェック")

    print("--サイズ--")
    row_size = len(problem["board"][0])
    column_size = len(problem["board"])
    board_size = row_size * column_size

    black_count = 0
    for line in problem["board"]:
        black_count += line.count(BLACKCELL)

    row_words_num = len(problem["row"])
    column_words_num = len(problem["column"])

    print("{}x{} = {}".format(row_size, column_size, board_size))
    print("black: {}, other: {}".format(black_count, board_size - black_count))
    print("words: {} (row: {} / column {})".format(
        row_words_num + column_words_num, row_words_num, column_words_num))
    print()

    print("--出現回数--")

    all_words = []
    for _, word in problem["row"] + problem["column"]:
        all_words.append(word)

    many_words = {}
    for word in all_words:
        if all_words.count(word) > 1:
            many_words[word] =  all_words.count(word)

    for word, count in many_words.items():
        print("{} appears {} times".format(word, count))

    if len(many_words) == 0:
        print("all words appear just once")


def main():
    parser = argparse.ArgumentParser(description='クロスワードの盤面から言葉を抜き出します')
    parser.add_argument('file', type=str,
                        help='クロスワードの盤面')
    parser.add_argument('--check', '-c', action='store_true',
                        help='言葉の重複などを調べます')

    args = parser.parse_args()

    input_board = load_file(args.file)
    if not validate(input_board):
        print("この盤面は加工できません。")
        for line in input_board:
            print(line)
        return 1

    problem = get_problem(input_board)

    if args.check:
        check_words(problem)
    else:
        show_problem(problem)

    return 0


if __name__ == '__main__':
    main()
