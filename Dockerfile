FROM python:3.10-alpine

WORKDIR /usr/src/boo_do

COPY ./requirements.txt /usr/src/boo_do/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/boo_do/requirements.txt

COPY ./app /usr/src/boo_do/app

CMD ["uvicorn", "app.main:boo_do", "--host", "0.0.0.0", "--port", "80"]