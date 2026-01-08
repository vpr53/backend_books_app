docker build -t book-web ./


docker run -it -p 8000:8000 --name book-web-instance book-web python project/manage.py runserver 0.0.0.0:8000