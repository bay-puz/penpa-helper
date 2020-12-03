# Puzzle Square JP
[Puzzle Square JP](https://puzsq.jp/main/index.php)の情報を取得する。

## contributors.py
作者別、パズル別の問題数を取得し、JSON形式で出力する。


Puzzle Square JPでは、URLで作者ID(?author=XXX)とパズルID(?puzzle=XXX)を同時に指定することで、その作者のそのパズルの一覧を見ることができる。
（この一覧はUIからはたどり着けないため、正式な機能ではないかもしれない。）
一覧画面にはパズル名・作者名・投稿件数が書かれているので、うまくパースして取得する。


## data/data.json
`contributors.py` で取得したすべての作者・パズルのデータをJSONの配列にしたもの。
ただし、問題数(count)が0のデータは省き、作者名(author.name)は取り除いている。


## wand-data/data.json
wandさんが公開しているPuzzle Square JPのデータをJSON形式に変換したもの。


## problems.py
パズル一覧のページから、問題のID、いいね数などを取得し、JSON形式で出力する。

Puzzle Square JPの一覧ページには、各問題のIDの他に、作者名、パズル名、いいね数、作成日時などが載っているため、それらをパースして取得する。

ページ毎にリクエストを投げるため、実行中に新しい問題が投稿されると、同じ問題が２回取得される。
プログラムの中ではチェックをしないので、実行後にIDを見て重複を取り除く必要がある。


## data/liked.csv
`problems.py` で取得した各問題のIDといいね数をCSV形式にしたもの。
wandさんが公開しているPuzzle Square JPのデータと合わせて使うことを想定している。
