FROM node:9.6.1 as builder
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
RUN npm install react-scripts@1.1.1 -g
COPY web/package.json /usr/src/app/package.json
RUN npm install

COPY web/public /usr/src/app/public
COPY web/src /usr/src/app/src
RUN npm run build

FROM tiangolo/uwsgi-nginx-flask:python3.6
EXPOSE 9090

RUN apt-get update && apt-get install libzbar-dev libzbar0 -y

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY api /app

RUN rm -rf /etc/nginx/conf.d
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /usr/src/app/build /app/static