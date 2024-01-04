#老師的 github
https://github.com/17app001/linebot
https://render.com/
gunicorn trainapp.wsgi

\*\*一定要在 base 底下(c+s+p)

#安裝 django 套件
pip install django

#建立專案
django-admin startproject 專案的名稱(假設是 ratebot)

#開啟目錄
open floder

#重開目錄，要開專案的目錄才對
ex:RATEBOT>ratebot>manage.py
這樣才對

#啟動 Server
python manage.py runserver

#修改語系
LANGUAGE_CODE='zh-Hant'
TIME_ZONE="Asia/Taipei"

#新增功能
python manage.py startapp main

from django.http import HttpResponse
'DIRS': [os.path.join(BASE_DIR, 'templates')]

python manage.py startapp login

python manage.py startapp test_html

#git 指令 1.安裝 git 2.專案目錄底下

#初始化本地倉庫
-git init

#產生忽略檔案

- .gitignore

#檔案屬性
-U->UnTack(尚未確認的)
-A->Added(新增的)
-M->Modified(修改的)

#加入控管
-git add<filename>
-git add .

- 加入所有版本控管/變動確認

#確認儲存

- git commit -am "異動訊息"
- git config --global user.email "peiyi523@gmail.com"
- git config --global user.name "peiyi"

#檢視狀態

- git status

#檢視 commit log
-git log
-git log --oneline

#綁定遠端倉庫
-git remote add origin https://github.com/peiyi523/ratebot.git(第一次時要這樣做)
-git remote -v(帶出當下綁定的是哪一個倉庫)

#推送資料到雲端
git push -u origin master

#複製專案

- git clone https://github.com/peiyi523/ratebot

#Channel secret
d36eb1d5f583fdad1ebce24c3f9ace05

#Channel access token
Y9OJcBnITGsZTxe2gMsoQpg4L8r9kqH9G26QgYaQS7bevmm1AXEBUicTyZaMtauBvD8WWX1VYsexjvgVGZKUokil3M+7VfadWYvwUoeekpxecCEiawIuTtm8oYeY7h2qQdmdeDi88gwY0oIOkuS40AdB04t89/1O/w1cDnyilFU=

#同步資料庫
python manage.py migrate

#同步雲端倉庫

- git push

#建虛擬環境
conda create -n django_env

# rich-menu 參考 github
