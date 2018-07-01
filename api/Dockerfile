FROM python:3.6.5-slim

RUN adduser api
WORKDIR /home/api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py config.py ./
COPY testzip ./

ENV FLASK_APP app.py
ENV API_SETTINGS="${API_SETTINGS}"
ENV MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD}"
RUN chown -R api:api ./
USER api

EXPOSE 5000:5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "--timeout", "5000", "--keep-alive", "75", "--threads", "8", "app:app"]
