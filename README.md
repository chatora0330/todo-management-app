# ToDo管理アプリ

Flask + SQLiteで作成したToDo管理Webアプリです。

Python / Flaskの学習を目的として、ユーザー認証からToDoのCRUD、
検索、絞り込み、並び替え、ページネーションまで実装しています。

## 概要

ユーザーごとにToDoを管理できるWebアプリです。

ログインしたユーザーは、自分のToDoを登録・編集・削除できます。

また、ToDoのステータスや優先度を設定したり、
検索・絞り込み・並び替えを行うことができます。

## 主な機能

- ユーザー登録
- ログイン・ログアウト
- パスワードのハッシュ化
- CSRF対策
- ToDoの登録
- ToDoの一覧表示
- ToDoの編集
- ToDoの削除
- ステータス変更
- 優先度設定
- 締切日設定
- タイトル検索
- ステータス絞り込み
- 優先度絞り込み
- 並び替え
- ページネーション
- ユーザーごとのToDo管理

## 使用技術

- Python
- Flask
- Flask-Login
- Flask-WTF
- WTForms
- SQLite
- Bootstrap
- HTML / CSS
- Git / GitHub

## セキュリティ

以下の対策を実装しています。

- パスワードのハッシュ化
- CSRF対策
- ログインユーザーのみToDo操作可能
- SQLのプレースホルダー使用
- ユーザーIDによるデータアクセス制御

## ディレクトリ構成

```text
project/
│
├── app.py
├── config.py
├── schema.sql
├── README.md
├── .gitignore
│
├── blueprints/
│   ├── __init__.py
│   ├── auth.py
│   └── todo.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── todo_list.html
│   ├── todo_add.html
│   └── todo_edit.html
│
└── static/
    └── css/
        └── style.css