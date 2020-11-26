# Puzzle Square JP
[Puzzle Square JP](https://puzsq.jp/main/index.php)の情報を取得する。

## contributors.py
作者別、パズル別の問題数を取得し、JSON形式で出力する。


実行例
```
$ python3 contributors.py --author_id 95 --puzzle_id 1 | jq .
{
  "author": {
    "id": 95,
    "name": "bay"
  },
  "puzzle": {
    "id": 1,
    "name": "スリザーリンク"
  },
  "count": 4
}
```

Puzzle Square JPでは、URLで作者ID(?author=XXX)とパズルID(?puzzle=XXX)を同時に指定することで、その作者のそのパズルの一覧を見ることができる。
（この一覧はUIからはたどり着けないため、正式な機能ではないかもしれない。）
一覧画面にはパズル名・作者名・投稿件数が書かれているので、うまくパースして取得する。

`--author_id`, `--puzzle_id`を指定すると、指定したIDのみを対象にする。
指定しなかった場合、すべての作者・パズルのデータを取得する。
ただし、存在しないID（author=20など）は省き、パズルの「その他」(puzzle=-1)は対象にする。

データを取得する際には、作者IDとパズルIDを指定したリクエストを投げる。
リクエストを投げる部分は並列化しているが、並列数を上げすぎるとサイトに影響が出るかもしれない。
また、リクエストが通らないことがたまにあるので、データの取得に失敗したときはIDをstderrに出力する。


## data/data.JSON
`contributors.py` で取得したすべての作者・パズルのデータをJSONの配列にしたもの。
ただし、問題数(count)が0のデータは省き、作者名(author.name)は取り除いている。
