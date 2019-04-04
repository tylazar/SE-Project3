FROM python:3
ENV APP /app

ADD . /code
WORKDIR /code

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uwsgi", "--ini", "app.ini" ]
