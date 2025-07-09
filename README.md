## Встановлення

cmd

git clone https://github.com/kettylike/blog-project.git
cd blog-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
(потрібно додати файл .env з токеном)
python manage.py migrate
python manage.py runserver/docker compose up --build
