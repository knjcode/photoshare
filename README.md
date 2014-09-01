# photoshare

## Overview

photoshare は写真や画像から簡単にWebギャラリーを作成するツールです。  
画像はサムネイルで画面に一覧表示され、サムネイルをクリックすることでlightboxによる
画像閲覧ができます。

## 必要環境

- python実行環境
- pythonスクリプトがCGIとして動作するサーバ環境
- pythonライブラリPILおよびexifread


## 事前準備

1. 本リポジトリのファイルを自分のWebサーバへコピーまたはクローン
2. config-sample.iniを適宜修正し、config.iniとして保存

## 使用方法

1. ギャラリーにしたい画像を格納したフォルダをWebサーバへアップロード
2. 対象フォルダ名を引数に prepics.py を実行

    $ python prepics.py \<target directory\>

3. Web経由で対象フォルダにアクセスするとフォトギャラリーを閲覧できます

## 仕組み

prepics.pyは引数に指定されたディレクトリ内の画像からサムネイルと画像情報を記録したCSVファイルを作成します。サムネイルはthumbnailsディレクトリ内に引数で指定されたディレクトリ名毎にファイル名先頭に"\_thumbs\_"を付与して作成します。
また、ギャラリー表示用のtemplate.pyを対象フォルダへindex.pyとしてコピーします。

画像情報CSVには、画像のEXIF情報から、画像の撮影日時・画像サイズ・撮影方向を記録して保存します。

### 設定ファイル詳細

prepics.py実行時の設定はconfig.iniファイルから読み込まれます。  
設定できる内容は以下のとおりです。

- ImageHeight  : サムネイル画像のサイズ
- Generated    : サムネイルおよびCSVファイル格納フォルダ名
- ImageQuality : サムネイル保存時の画像圧縮率

### CSVファイル概要

#### sort_datetime.csv

撮影日時の昇順

#### sort_datetime_reverse.csv

撮影日時の降順

#### sort_filedate.csv

ファイルのタイムスタンプの昇順

#### sort_filedate_reverse.csv

ファイルのタイムスタンプの降順
