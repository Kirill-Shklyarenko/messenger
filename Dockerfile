FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /karuna
WORKDIR /karuna
ADD . /karuna/
RUN pip install -r requirements.txt
