# -*- coding: utf-8 -*-
import argparse
import math


def load_words(file: str) -> list:
    fopen = open(file)
    text = fopen.read()

    words = text.splitlines()
    words_filtered = []
    for word in words:
        if len(word) != 0 and word[0] != '!':
            words_filtered.append(word)

    return words_filtered


def adjust_width(num: int) -> str:
    if num < 10:
        return ' ' + str(num)

    return str(num)


def trans_problem(words: list):
    all_chara = []
    for word in words:
        for _, chara in enumerate(word):
            all_chara.append(chara)

    chara_id = {}
    chara_chara = {}
    answer_list = {}
    for chara in all_chara:
        count = all_chara.count(chara)
        if count == 1:
            chara_id[chara] = '  '
            chara_chara[chara] = chara
        elif list(chara_id).count(chara) == 0:
            num = len(answer_list) + 1
            answer_list[num] = chara
            chara_id[chara] = adjust_width(num)
            chara_chara[chara] = '＿'

    table_id = str.maketrans(chara_id)
    table_chara = str.maketrans(chara_chara)

    problem_chara = {}
    problem_id = {}
    for row, word in enumerate(words):
        word_space = ""
        for _, chara in enumerate(word):
            word_space += ' ' + chara

        problem_id[row] = word_space.translate(table_id)
        problem_chara[row] = word_space.translate(table_chara)

    return problem_chara, problem_id, answer_list


def show_words(charas: dict, ids: dict) -> None:
    column = math.ceil(len(charas) / 4)
    for i in range(0, column):
        str_charas = charas[i]
        str_ids = ids[i]
        for j in [1, 2, 3]:
            count = j * column + i
            if count >= len(charas):
                break
            word_left = (j - 1) * column + i
            space = "   " * (6 - int(len(charas[word_left]) / 2))
            str_charas += space + charas[count]
            str_ids += space + ids[count]
        print(str_charas)
        print(str_ids)
        print()


def show_list(answer: dict, show_answer: bool):
    ans_column = math.ceil(len(answer) / 17)
    ans_row = math.ceil(len(answer) / ans_column)
    ans_top = '┏'
    ans_middle = '┠'
    ans_bottom = '┗'
    ans_num = '┃'
    ans_chara = '┃'
    for num, chara in answer.items():
        ans_num += adjust_width(num) + '┃'
        if not show_answer:
            chara = '　'
        ans_chara += chara + '┃'
        if num % ans_row == 0 or num == len(answer):
            ans_top += '━┓'
            ans_middle += '─┨'
            ans_bottom += '━┛'
            print(ans_top)
            print(ans_num)
            print(ans_middle)
            print(ans_chara)
            print(ans_bottom)
            ans_top = '┏'
            ans_middle = '┠'
            ans_bottom = '┗'
            ans_num = '┃'
            ans_chara = '┃'
        else:
            ans_top += '━┳'
            ans_middle += '─╂'
            ans_bottom += '━┻'


def show_problem(words: list, show_answer: bool) -> None:
    charas, ids, answer = trans_problem(words)

    print("漢字抜け熟語")
    if show_answer:
        print("解答")
    print()

    if not show_answer:
        show_words(charas, ids)
    show_list(answer, show_answer)


def analysis(words: list) -> None:
    print("==統計情報==")

    all_chara = []
    all_kind_chara = []
    for word in words:
        for _, chara in enumerate(word):
            all_chara.append(chara)
            if chara not in all_kind_chara:
                all_kind_chara.append(chara)

    chara_count = {}
    for chara in all_kind_chara:
        count = all_chara.count(chara)
        if count in chara_count:
            chara_count[count] += chara
        else:
            chara_count[count] = chara

    print("--サイズ--")
    print("文字数: {}, 単語数: {}".format(len(all_chara), len(words)))
    num_hint = len(chara_count[1])
    num_hidden = len(all_kind_chara) - num_hint
    print("種類: {} (ヒント: {}, 抜け: {})".format(
        len(all_kind_chara), num_hint, num_hidden))
    print()

    print("--出現回数--")
    for count, charas in sorted(chara_count.items()):
        print("{}: {} ({})".format(count, charas, len(charas)))
    print()

    print("--利用数--")
    for word in words:
        print("{}: ".format(word), end="")
        score = 0
        for _, chara in enumerate(word):
            count_other = all_chara.count(chara) - 1
            score += count_other
            print("{}".format(count_other), end="")
        print(" = {}".format(score))
    print()

    print("--ヒント数--")
    count_hint = {}
    for word in words:
        word_count_hint = 0
        for _, chara in enumerate(word):
            if all_chara.count(chara) == 1:
                word_count_hint += 1
        if word_count_hint in count_hint:
            count_hint[word_count_hint] += 1
        else:
            count_hint[word_count_hint] = 1
    for hint, count in count_hint.items():
        print("hint {}: {} words".format(hint, count))
    print()

    print("--包含関係--")
    count_include = 0
    for word in words:
        other_words = {}
        hidden_charas = 0
        for _, chara in enumerate(word):
            if all_chara.count(chara) == 1:
                continue
            hidden_charas += 1
            for word_2 in words:
                if word_2 != word and chara in word_2:
                    if word_2 in other_words:
                        other_words[word_2] += 1
                    else:
                        other_words[word_2] = 1
        for other_word, count in other_words.items():
            if count == hidden_charas:
                count_include += 1
                print("{} is in {}".format(word, other_word))

    if count_include == 0:
        print("なし")


def main():
    parser = argparse.ArgumentParser(description='漢字抜け熟語を出題用に整形します')
    parser.add_argument('file', type=str,
                        help='漢字の言葉を並べたファイル')
    parser.add_argument('--statics', '-s', action='store_true',
                        help='文字の出現数などを表示します')
    parser.add_argument('--show-answer', '-a', action='store_true',
                        help='解答を表示します')

    args = parser.parse_args()

    words = load_words(args.file)
    if args.statics:
        analysis(words)
    else:
        show_problem(words, args.show_answer)


if __name__ == '__main__':
    main()
