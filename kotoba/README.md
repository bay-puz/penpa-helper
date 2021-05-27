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
### 豚辞書
本家（第12版）の配布場所は[豚辞書の詳細情報 : Vector ソフトを探す！](https://www.vector.co.jp/soft/dl/dos/game/se018509.html)だが、より新しい第14版を[【非公式】豚辞書 第14版【再頒布】](https://kinosei.ml/2015/02/11/%E3%80%90%E9%9D%9E%E5%85%AC%E5%BC%8F%E3%80%91%E8%B1%9A%E8%BE%9E%E6%9B%B8-%E7%AC%AC14%E7%89%88%E3%80%90%E5%86%8D%E9%A0%92%E5%B8%83%E3%80%91/)で再配布している。
ここでは第14版を使う。

#### リスト化
```
python normalize.py butah014/buta014.dic > list/buta.txt
```

#### 改変・再配布について
permit.docに、「当アーカイブ・ファイルの内容に一切の変更を加えず、オリジナルのまま」であれば自由に再配布して良く、また、引用・抽出などしたデータ集を公開する場合は「結果として出来上がったデータ集の付属ドキュメントに当豚辞書から｛引用、参照、抜出、抽出、改造、‥‥｝した旨の記載」をするように書いてある。

豚辞書のアーカイブ(butah014)を再配布し、butah014/buta014.dicを変形したリスト(list/buta.txt)を公開する。


### nico-pixiv
[ncaq/dic-nico-intersection-pixiv](https://github.com/ncaq/dic-nico-intersection-pixiv)

#### リスト化
```
curl https://cdn.ncaq.net/dic-nico-intersection-pixiv.txt > np.dat
python normalize.py --ime np.dat > list/nico-pixiv.txt
```

#### ライセンスについて
生成物(dic-nico-intersection-pixiv.txt)の著作権を主張しないと宣言しているので、加工物(list/nico-pixiv.txt)を公開します。

> 生成物はスクレイピング結果を利用している都合上、 著作権は主張しません。


### 漢字四文字言葉集
[漢字四文字言葉集](http://nikolist.jpn.org/puzzle/kanjinuke/)

#### リスト化
```
curl http://nikolist.jpn.org/puzzle/kanjinuke/yojijukugo.txt > yoji.dat
nkf --overwrite -w yoji.txt
python3 normalize.py -k2 yoji.dat > list/yojijukugo.txt
```

#### ライセンスについて
list/yojijukugo.txt は[CC BY-NC-SA 2.1 JP](https://creativecommons.org/licenses/by-nc-sa/2.1/jp/)に準拠する。
元データがこのライセンスに準拠しているため。

> プログラムのソースなどはクリエイティブコモンズの帰属・非営利・同一条件配布に準拠。
> http://nikolist.jpn.org/index.html
