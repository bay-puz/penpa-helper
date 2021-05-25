# 言葉リスト
言葉系パズルで使うためのリスト。

内容や形式は[豚辞書](https://www.vector.co.jp/soft/dl/dos/game/se018509.html)をまねています。


## リストの形式
ひらがなの言葉を改行で並べる。
ソートは文字数順、同じ文字数の言葉は文字コード順。

知名度の高い名詞を集めたいが、それ以外の言葉も排除しない。ただし1文字の言葉は入れない。


## 文字種
文字はひらがなを使い、さらに文字種を制限する。特殊なひらがなは変換してから採録する。

| 変換元 | 変換先 |
| ---- | ---- |
| ぁぃぅぇぉゃゅょっゎヵヶ | あいうえおやゆよつわかけ |
| ヴァヴィヴヴェヴォヴャヴュヴョ | ばびぶべぼびゃびゅびょ |
| ゐゑ | いえ |


## 元データ
### nico-pixiv
[ncaq/dic-nico-intersection-pixiv](https://github.com/ncaq/dic-nico-intersection-pixiv)

#### 変換
```
curl https://cdn.ncaq.net/dic-nico-intersection-pixiv.txt > np.dat
python normalize.py --ime np.dat > list/nico-pixiv.txt
```

#### ライセンスについて
生成物(dic-nico-intersection-pixiv.txt)の著作権を主張しないと宣言しているので、加工物(list/nico-pixiv.txt)を公開します。

> 生成物はスクレイピング結果を利用している都合上、 著作権は主張しません。
