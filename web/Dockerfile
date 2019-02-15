
# base image
FROM node:11.6.0 as builder

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install and cache app dependencies
COPY package*.json /usr/src/app/
RUN npm install

# add app
COPY . /usr/src/app

RUN npm build

##################
### production ###
##################

# base image
FROM nginx:1.13.9-alpine

# copy artifact build from the 'build environment'
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

# run nginx
CMD ["nginx", "-g", "daemon off;"]
