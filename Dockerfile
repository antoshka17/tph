FROM python:3.10.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

COPY . /code/

RUN pip install -r ./requirements.txt

EXPOSE 8000
