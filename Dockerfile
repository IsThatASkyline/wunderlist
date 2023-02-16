FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:$PORT
