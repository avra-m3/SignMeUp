The SignMeUp Project
===
### About
The aim of this project is to provide an easy environment through which clubs can sign up members simply by providing an RMIT student ID card.

The future scope of this project may allow for alternate sign up methods and/or card providers.

Project Structure
----
This project consists of 2 core components;
 * API (Backend)
    * Written in flask, this component provides state and character recognition services to the front end web provider.
 * Web (Frontend)
    * Written in react this part of the application provides a frontend by which a user easily provide a student card image to the API and sign up to a given club.


Deployment
---
This project uses a production deployment of Docker but can be developed without it.

### Development Environment
In the development environment each component should be testable without connecting the others. 
#### API
Use of the development environment requiresthe following

1. A set of GCloud OAuth2 credentials with access to Storage Buckets and Cloud vision API's

2. A Google Cloud storage bucket


##### Environment Variables

**GOOGLE_APPLICATION_CREDENTIALS**: The path to application credentials JSON for cloud vision

**DATABASE_URI\***: The database URI see SQLAlchemy documentation for more information https://docs.sqlalchemy.org/en/latest/core/engines.html

**SECRET_KEY\*** This key is used for password encryption, please set it otherwise anyone will be able to unhash passwords your database with the default "Quack Quack" secret key

\* *Optional*

**Debug\*** This Doesn't do anything yet but will soon!


##### Endpoints
For information regarding the various endpoints please see the postman documentation.

https://documenter.getpostman.com/view/3609222/RzZ1sPcW

### Docker

Docker support is part of release 1.0 but not currently tested.
