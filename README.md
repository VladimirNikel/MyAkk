﻿# Менеджер паролей MyAkk

## Инструкция по развертыванию сервера

1. Сначала необходимо установить следующее программное обеспечение на Ваш компьютер: Python 2.7 или более поздняя версия, Django 2.1.4, библиотека cryptography для Python, библиотека psycopg2 для Python, система контроля версий Git, СУБД PostgreSQL.
	- Python может быть установлен с официального сайта https://www.python.org/getit/windows/
	- Пакеты Django и cryptography могут быть установлены с помощью установщика pip. Для этого необходимо в командной строке Windows (cmd) выполнить следующие команды:
		- pip install django
		- pip install cryptography
		- pip install psycopg2
	- Система Git также может быть скачана с официального сайта https://git-scm.com/download
	- СУБД PostgreSQL может быть загружена с официального сайта разработчика https://www.postgresql.org/download/ и устанолвена станартным способом установки приложений с помощью исполняемого файла
2. Далее необходимо создать пустую базу данных в СУБД PostgreSQL. Для этого нужно:
	- В папке, в которой установлена СУБД перейти по пути .\PgAdmin4\bin\ и открыть программу pgadmin4.exe
	- Далее, воспользовавшись графическим интерфейсом программы, необходимо создать пустую базу данных
3. Теперь следует открыть программу Git bash в той папке, в которую предполагается поместить проект и выполнить команду git clone https://github.com/VladimirNikel/MyAkk
4. Далее необходимо настроить БД для сервера:
	- Перейти в папку Server\Password manager\ и, открыв файл settings.py с помощью текстового редактора, записать в поле DATABASES параметры своей базы данных и соданного пользователя
	- Перейти оратно в папку Server и выполнить из cmd команды:
		- python manage.py makemigrations
		- python manage.py migrate
5. Теперь, открыв cmd той же папке, необходимо выполнить всего одну команду: python manage.py runserver 
Инструкция по запуску тестов сервера
1. Выполнить пункты 1-2 из инструкции по развертыванию сервера
2. Теперь, открыв cmd той же папке, необходимо выполнить всего одну команду: python manage.py test