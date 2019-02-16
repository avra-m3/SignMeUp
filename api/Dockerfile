FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN apt update && apt install -y libzbar0 tesseract-ocr

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./ /app/