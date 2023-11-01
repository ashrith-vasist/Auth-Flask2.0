FROM python:3-alpine3.9

WORKDIR /app
COPY . /app


RUN  pip3 install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator bootstrap_flask

EXPOSE 5000
#ENV NAME World

CMD [ "python3", "src/app.py" ]