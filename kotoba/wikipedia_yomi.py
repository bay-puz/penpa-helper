# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


# かな文字（全角等号は人名に使われる）
KANA_PATTERN = '[ぁ-ヿ 　＝]'

def is_kana(char: str) -> bool:
    return re.fullmatch(KANA_PATTERN, char)


def is_kana_word(word: str) -> bool:
    for c in word:
        if not is_kana(c):
            return False
    return True


def is_worthful(word: str) -> bool:
    # 空白またはかな1文字は除外
    if len(word) < 1 or is_kana(word):
        return False

    # 一覧と日付は除外する
    denied_patterns = ['.+一覧', '[0-9]+年代', '[0-9]+年', '[0-9]+月[0-9]+日']
    for pat in denied_patterns:
        if re.fullmatch(pat, word):
            return False

    return True


def trim_title(word: str) -> str:
    # "Wikipedia: "を削る
    title_prefix = 'Wikipedia: '
    word = word.replace(title_prefix, '')

    # "（曖昧さ回避）"などを削る
    trim_pattern = '[ 　]?[（(].+[）)]'
    searched = re.search(trim_pattern, word)
    if searched:
        word= word[:searched.start()]
    return word


def get_yomi_by_yomigana(abst: str) -> str:
    # abstractが"|よみがな = こうもくめい"のときに読み仮名を取る
    yomigana_prefix = "\|よみがな = "
    yomigana_pattern = yomigana_prefix + KANA_PATTERN + '+'
    if re.fullmatch(yomigana_pattern, abst):
        return re.sub(yomigana_prefix, '', abst)

    return ''


def get_yomi_by_parenthesis(abst: str, title: str) -> str:
    abst = abst.replace(' ', '').replace('　', '')
    abst = abst.replace('(', '（').replace(')', '）')

    # "この項目名（こうもくめい）では、〜"といったabstractを除外
    deha_pattern = '）(一覧)?では'
    searched = re.search(deha_pattern, abst)
    if searched:
        if re.search('）', abst).start() == searched.start():
            return ''

    # "項目名（こうもくめい、名詞）は〜"といった文から読み仮名を取る
    yomi_prefix = re.escape(title) + '（'
    yomi_suffix = '[）、，,]'
    yomi_pattern = yomi_prefix + KANA_PATTERN + '+' + yomi_suffix
    searched= re.search(yomi_pattern, abst)
    if searched is None:
        return ''

    yomi = searched.group(0)
    yomi = re.sub(yomi_prefix, '', yomi)
    yomi = re.sub(yomi_suffix, '', yomi)

    # 2つ以上の読みを"もしくは"でつなげている場合があるので、最初の読みを取る
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
