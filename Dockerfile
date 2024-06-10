FROM python:3.12.2
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code/melp
COPY requirements.txt /code/
RUN pip install -r ../requirements.txt
# RUN pip install psycopg2cffi==2.8.1

CMD python manage.py runserver_plus 0.0.0.0:8000
