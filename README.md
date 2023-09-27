![example workflow](https://github.com/viva-lavita/foodgram-project-react/actions/workflows/main.yml/badge.svg)

[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru)

# Продуктовый помощник Foodgram
«Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать и скачивать готовый список продуктов, которые нужно купить для приготовления выбранных блюд. 

Данный проект - это полностью рабочая платформа, разработанная с использованием Django в качестве бэкенд-фреймворка и React в качестве фронтенд-библиотеки. Деплой на сервер реализован с помощью контейнизатора приложений Docker и технологии автоматизации тестирования и доставки новых модулей проекта - CD/CI.

Вся система обеспечивает безопасность данных пользователей, используя механизм аутентификации и авторизации Djoser, а использование обновленной версии Django 4.2.5, обеспечивает усиленную безопасность передачи данных.

Этот проект может быть запущен на сервере или на локальной машине после установки всех зависимостей. В дополнение к тому, это открытый исходный код, поэтому вы можете адаптировать его под свои потребности или вносить свои изменения.

![Иллюстрация к проекту](https://github.com/viva-lavita/foodgram-project-react/blob/master/foodgram_picture.png)

***
Данный проект временно запущен и доступен по адресу https://kittygram-lavita.ddns.net/, вы можете зайти и ознакомиться с функционалом. 

Креды к проекту: \
login: admin \
password: qf1478951f 
***

## Tecnhologies

- Python 3.11.5
- Django 4.2.5
- Django REST framework 3.14
- Nginx
- Docker
- Djoser
- Postgres

  \* Полный список библиотек в файле requirements.txt

# Порядок запуска
## Запуск проекта локально
Клонировать репозиторий и перейти в него:
```
git@github.com:viva-lavita/foodgram-project-react.git
```

Перейдите в папку проекта и создайте/активируйте виртуальное окружение, обновите pip и установите зависимости:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

В корне проекта создайте файл .env cо следующим содержимым:
 
- SECRET_KEY='секретный код вашего проекта из файла settings'
- DEBUG=True
- ALLOWED_HOSTS='IP вашего сервера и его доменное имя 127.0.0.1 localhost'
- CSRF_TRUSTED_ORIGINS='https://доменное_имя_вашего_проекта'
- CORS_ORIGIN_WHITELIST='https://доменное_имя_вашего_проекта'
- POSTGRES_DB='foodgram'
- POSTGRES_USER='юзернейм пользователя бд'
- POSTGRES_PASSWORD='пароль'
- DB_HOST='db'
- DB_PORT='5432'

Далее перейдите в папку infra/ и запустите локальную версию сайта.
```
docker-compose -f docker-compose.local.yml up
```

Сделайте миграции, соберите статику, создайте суперюзера и наполните базу ингредиентами. 
```bash
docker compose -f docker-compose.local.yml exec backend python manage.py migrate
docker compose -f docker-compose.local.yml exec -it backend python manage.py collectstatic --no-input
docker compose -f docker-compose.local.yml exec backend python manage.py load_csv --path=data/ingredients.csv --model_name=Ingredient --app_name=recipes
docker compose -f docker-compose.local.yml exec backend python manage.py createsuperuser
```

Теперь локальная версия сайта полностью готова к эксплуатации. \
Со всеми доступными эндпоинтами можно ознакомиться по адресу: 
```
http://127.0.0.1:8000/api/docs/
```

Остановка проекта:
```
docker compose down
```


## Запуск проекта на удаленном сервере

Форкните и клонируйте репозиторий
```
git clone git@github.com:ваш-логин/foodgram-project-react.git
```

Перейдите в папку проекта и создайте/активируйте виртуальное окружение, обновите pip и установите зависимости:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

Сбилдите образа и залейте их на dockerhub, обратите внимание, образ foodgram_nginx собирается на основании папки infra/. \
Вместо username подставьте свой username на dockerhub.
```
cd frontend
docker build -t username/foodgram_frontend .
cd ../backend
docker build -t username/foodgram_backend .
cd ../infra
docker build -t username/foodgram_nginx .

docker push username/foodgram_frontend
docker push username/foodgram_backend
docker push username/foodgram_nginx
```

Подключитесь к удаленному серверу
```
ssh <server user>@<server IP>
```

Установите Докер на удаленный сервер
```
sudo apt install docker.io
```

Установите Docker Compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Получение разрешений для docker-compose
```text
sudo chmod +x /usr/local/bin/docker-compose
```

Перейдите в рабочую директорию и создайте папку проекта
```
cd
mkdir foodgram && cd foodgram/
touch .env
```

Создайте файл .env
```
touch .env
```
 Со следующим содержимым:
 
- SECRET_KEY='секретный код вашего проекта из файла settings'
- DEBUG=True
- ALLOWED_HOSTS='IP вашего сервера и его доменное имя 127.0.0.1 localhost'
- CSRF_TRUSTED_ORIGINS='https://доменное_имя_вашего_проекта'
- CORS_ORIGIN_WHITELIST='https://доменное_имя_вашего_проекта'
- POSTGRES_DB='foodgram'
- POSTGRES_USER='юзернейм пользователя бд'
- POSTGRES_PASSWORD='пароль'
- DB_HOST='db'
- DB_PORT='5432'


Скопируйте файл docker-compose.yml в директорию foodgram/
```
scp -r infra/docker-compose.yml <server user>@<server IP>:/home/<server user>/foodgram/
```  

Откройте настройки внешнего nginx
```
sudo nano /etc/nginx/sites-enabled/default
```
И пропишите настройки
```
server {
    server_tokens off;

    server_name доменное_имя_вашего_проекта;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
```

Проверьте корректность настроек и перезапустите nginx
```
sudo nginx -t
sudo systemctl reload nginx
```

Для получения сертификата для https протокола, нужно установить certbot, для его установки вам понадобится пакетный менеджер snap. Установите его и завсимость командами:
```
sudo apt install snapd 
sudo snap install core; sudo snap refresh core

# При успешной установке зависимостей в терминале выведется:
# core 16-2.58.2 from Canonical✓ installed  
```

Установка пакета certbot.
```
sudo snap install --classic certbot

# При успешной установке пакета в терминале выведется:
# certbot 2.3.0 from Certbot Project (certbot-eff✓) installed
```

Создайте ссылки на certbot в системной директории, чтобы у пользователя с правами администратора был доступ к этому пакету.
```
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Запустите certbot и получите SSL-сертификат
```
sudo certbot --nginx
```
Далее система будет просить вас написать почту, согласиться с условиями и т.п. сделайте все запрашиваемое.

Перезагрузите конфигурацию Nginx:
```
sudo systemctl reload nginx
```

 Запустите docker-compose
```
sudo docker-compose up -d
```

Сделайте миграции, соберите статику, создайте суперюзера и наполните базу ингредиентами. 
```bash
sudo docker compose -f docker-compose.local.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.local.yml exec -it backend python manage.py collectstatic --no-input
sudo docker compose -f docker-compose.local.yml exec backend python manage.py load_csv --path=data/ingredients.csv --model_name=Ingredient --app_name=recipes
sudo docker compose -f docker-compose.local.yml exec backend python manage.py createsuperuser
```

Теперь на сервере крутится целый флот контейнеров, объединённых в сеть. Docker Compose работает в фоне, но в любой момент готов принять ваши команды. Выполнять команды docker compose нужно из той директории, в которой размещён файл конфигурации.
Основные команды, которые вам понадобятся для управления:

- sudo docker compose stop — остановит все контейнеры, но оставит сети и volume. Эта команда пригодится, чтобы перезагрузить или обновить приложения.
- sudo docker compose down — остановит все контейнеры, удалит их, сети и анонимные volumes. Можно будет начать всё заново.
- sudo docker compose logs — просмотр логов запущенных контейнеров.

Проверьте, что все нужные контейнеры запущены:
```
sudo docker compose -f docker-compose.production.yml ps
```

Удаленная версия сайта полностью готова к эксплуатации. \
Со всеми доступными эндпоинтами можно ознакомиться по адресу: 
```
'https://доменное_имя_вашего_проекта'/api/docs/
```

Остановка проекта:
```
sudo docker compose down
```

## Запуск функционала автоматизации тестирования и доставки новых модулей проекта - CD/CI.

Для использования этого функционала вам нужно будет:
1. Форкнуть репозиторий, перейти в Settings проекта -> Secrets and variables -> Action или по ссылке: \
https://github.com/ваш_логин/foodgram-project-react/settings/secrets/actions

2. Создайте виртуальные переменные такие же как и в вашем файле .env на удаленном сервере и плюс еще несколько:    
- TELEGRAM_TO - id вашего аккаунта в телеграмм. 
- TELEGRAM_TOKEN - токен бота (можно зарегистрировать у botfather), не забудьте начать с ним диалог, так как бот не может первым начать беседу. 
- SSH_PASSPHRASE - пароль к рабочему серверу. 
- USER - ваш логин учетки рабочего сервера. 
- SSH_KEY - закрытый ключ. 
- HOST - IP рабочего сервера. 
- DOCKER_USERNAME - логин вашего dockerhub. 
- DOCKER_PASSWORD - пароль вашего dockerhub.

Теперь после push в ветку master ваш код будет автоматически тестироваться flake8 и деплоиться на рабочий сервер, после удачного деплоя вам автоматически будет приходить сообщение от вашего телеграмм бота. 

Приятного аппетита =)

### Автор 
- Сопина Виктория - [GitHub](https://github.com/viva-lavita)
