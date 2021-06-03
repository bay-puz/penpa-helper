# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


# かな文字（全角等号は人名に使われる）
KANA_PATTERN = '[ぁ-ヿ 　＝]'


def is_kana(char: str) -> bool:
    return re.fullmatch(KANA_PATTERN, char)


def is_kana_word(word: str) -> bool:
    for char in word:
        if not is_kana(char):
            return False
    return True


def is_worthful(word: str) -> bool:
    """
    言葉として適しているどうかを判定する
    - 空白またはかな1文字はFalse
    - 一覧、年代、日付はFalse
    """

    if len(word) < 1 or is_kana(word):
        return False

    denied_patterns = ['.+一覧', '[0-9]+年代', '[0-9]+年', '[0-9]+月[0-9]+日']
    for pat in denied_patterns:
        if re.fullmatch(pat, word):
            return False

    return True


def trim_title(word: str) -> str:
    """
    titleタグから余分な文字を削る
    - 先頭の"Wikipedia: "を削る
    - " (曖昧さ回避)"のように括弧があれば削る
    """

    title_prefix = 'Wikipedia: '
    word = word.replace(title_prefix, '')

    trim_pattern = '[ 　]?[（(].+[）)]'
    searched = re.search(trim_pattern, word)
    if searched:
        word = word[:searched.start()]
    return word


def get_yomi_by_yomigana(abst: str) -> str:
    """
    abstractタグにTemplateの"よみがな"が入ることがあるのでそれを取り出す
    """

    yomigana_prefix = re.escape("|よみがな = ")
    yomigana_pattern = yomigana_prefix + KANA_PATTERN + '+'
    if re.fullmatch(yomigana_pattern, abst):
        return re.sub(yomigana_prefix, '', abst)

    return ''


def get_yomi_by_parenthesis(abst: str, title: str) -> str:
    """
    abstractの冒頭に"項目名（読み仮名）"と書かれるのでそれを取り出す
    - "項目名（こうもくめい）では、〜"といったabstractの場合は、
    　項目名が語ではないことが多いので除外する
    - 読み仮名と閉じ括弧のあいだに別の語がある場合は削る
    - 2つ以上の読みを"もしくは"などでつなげている場合は最初の読みを取る

    """
    abst = abst.replace(' ', '').replace('　', '')
    abst = abst.replace('(', '（').replace(')', '）')

    deha_pattern = '）(一覧)?では'
    searched = re.search(deha_pattern, abst)
    if searched:
        if re.search('）', abst).start() == searched.start():
            return ''

    yomi_prefix = re.escape(title) + '（'
    yomi_suffix = '[）、，,]'
    yomi_pattern = yomi_prefix + KANA_PATTERN + '+' + yomi_suffix
    searched = re.search(yomi_pattern, abst)
    if searched is None:
        return ''

    yomi = searched.group(0)
    yomi = re.sub(yomi_prefix, '', yomi)
    yomi = re.sub(yomi_suffix, '', yomi)

    deliminate_words = ['もしくは', 'または']
    for deliminator in deliminate_words:
        searched = re.search(deliminator, yomi)
        # 項目名に含まれるときは除く
        if searched and not re.search(deliminator, title):
            yomi = yomi[:searched.start()]

    return yomi


def get_yomi(abst: str, title: str) -> str:
    yomi = get_yomi_by_yomigana(abst)
    if len(yomi) > 0:
        return yomi

    return get_yomi_by_parenthesis(abst, title)


def parse_title(xml_line: str) -> str:
    soup = BeautifulSoup(xml_line, 'lxml-xml')

    title = soup.find('title')
    if title is None or len(title.contents) == 0:
        return ''

    return trim_title(title.contents[0])


def find_title(xml_line: str) -> str:
    if not re.search('title', xml_line):
        return ''

    title = parse_title(xml_line)
    if len(title) > 0 and is_worthful(title):
        return title
    return ''


def parse_abstract(xml_line: str, title: str) -> (bool, str):
    soup = BeautifulSoup(xml_line, 'lxml-xml')

    abst = soup.find('abstract')
    if not abst or len(abst.contents) == 0:
        return False, ''

    return True, get_yomi(abst.contents[0], title)


def find_yomi(xml_line: str, latest_title: str) -> str:
    if len(latest_title) < 1:
        return ''

    is_parsed, yomi = parse_abstract(xml_line, latest_title)
    if is_parsed:
        if is_worthful(yomi) and is_kana_word(yomi):
            return yomi
    return ''


def load_xml(file_name: str) -> list:
    with open(file_name) as file:
        return file.read().splitlines()


def main():
    file_name = 'test.xml'
    lines = load_xml(file_name)

    latest_title = ''
    for line in lines:
        title = find_title(line)
        if len(title) > 0:
            if is_kana_word(title):
                print(title)
            else:
                latest_title = title
            continue

        yomi = find_yomi(line, latest_title)
        if len(yomi) > 0:
            print(yomi)


if __name__ == '__main__':
    main()
