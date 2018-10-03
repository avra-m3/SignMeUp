FROM tiangolo/uwsgi-nginx-flask:python3.6
ENV LISTEN_PORT 9090
EXPOSE 9090

RUN apt-get update && apt-get install libzbar0 -y

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY api /app
COPY nginx.conf /etc/nginx/conf.d/upload.conf

