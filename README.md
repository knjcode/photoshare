# photoshare

## Overview

photoshare は写真や画像から簡単にウェブギャラリーを作成するスクリプト群です。
画像はサムネイルで画面に一覧表示され、サムネイルをクリックするとlightboxによる
画像閲覧ができます。

## 使用方法

レポジトリのファイルを自分のWebサーバへコピー
ギャラリーにしたい画像を格納したフォルダをアップロード
アップロードしたフォルダ内にindex.cgiをコピーして配置
アップロードしたフォルダ名を引数に pripics.py を実行
index.cgiにアクセスするとフォトギャラリーを閲覧できます。

## 仕組み

pripics.pyは引数に指定されたディレクトリ内にサムネイルと画像情報を記録したCSVを作成します。
サムネイルはthumbnailsディレクトリ内にファイル名先頭に"_thumbs_"を付与して作成します。
画像情報CSVは、画像のEXIF情報から、画像の撮影日時・画像サイズ・撮影方向を記録して保存します。

## CSVファイル詳細

### sort_datetime.csv

撮影日時の昇順

### sort_datetime_reverse.csv

撮影日時の降順

### sort_filedate.csv

ファイルのタイムスタンプの昇順

### sort_filedate_reverse.csv

ファイルのタイムスタンプの降順
