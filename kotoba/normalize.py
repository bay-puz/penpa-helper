# -*- coding: utf-8 -*-
import argparse


def load_ime(file_name: str) -> list:
    with open(file_name) as file:
        ime = file.read().splitlines()
        words = []
        for line in ime:
            if len(line) == 0 or line[0] == '#':
                continue
            word = line.split()[0]
            words.append(word)
        return words


def kata_to_hira(char: str) -> str:
    if ord("ァ") <= ord(char) <= ord("ヶ"):
        return chr(ord(char) - 96)
    return char


def convert_hira(word: str) -> str:
    def _convert_char(char: str):
        str_before = "ぁぃぅぇぉゕゖっゃゅょゎゐゑ"
        str_after = "あいうえおかけつやゆよわいえ"
        if char in str_before:
            return str_after[str_before.index(char)]
        return char

    converted = ''
    i = 0
    while i < len(word):
        str_aieo = 'ぁぃぇぉ'
        str_yayuyo = 'ゃゅょ'
        str_b = 'ばびべぼ'
        if word[i] == 'ゔ':
            if i == len(word) - 1 or word[i+1] not in str_aieo + str_yayuyo:
                converted += 'ぶ'
            else:
                if word[i+1] in str_aieo:
                    converted += str_b[str_aieo.index(word[i+1])]
                    i += 1
                else:
                    converted += 'び'
        else:
            converted += _convert_char(word[i])
        i += 1

    return converted


def sort_buta(words: list) -> list:
    return sorted(sorted(set(words)), key=len)


def main():
    parser = argparse.ArgumentParser(description='言葉リストを正規化する')
    parser.add_argument('file', type=str, help='入力ファイル')
    parser.add_argument('--ime', action='store_true', help='IMEファイルを変換')
    args = parser.parse_args()

    if args.ime:
        ime_words = load_ime(args.file)
        words = []
        for word in ime_words:
            words.append(convert_hira(word))

        words = sort_buta(words)
        for word in words:
            if len(word) < 2:
                continue
            print(word)


if __name__ == '__main__':
    main()
