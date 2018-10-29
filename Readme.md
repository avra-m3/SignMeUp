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
Use of the development environment requires (all of*) the following

\*
*Temporary; Will consolidate cloud vision module to use OAuth2 as well.*

1. An API Key with access to use the google cloud vision API.

2. An OAuth2 for use with google cloud storage 

3. A google cloud storage bucket called csit-cache (need to make this configurable) with public access (will be changed with consolidation of authentication)


##### Environment Variables

**OCR_AUTH_KEY**: The API token for use with cloud vision

**GOOGLE_APPLICATION_CREDENTIALS**: The path to application credentials for cloud vision

**DATABASE\***: One of 'sqlite', 'mysql', 'postgre' This determines the database provider.

**DATABASE_CONFIG\*** Required if using anything but sqlite, should be a json object providing all required fields for the database.
SEE: http://docs.peewee-orm.com/en/latest/peewee/database.html#using-mysql for more information

\* *Optional*


##### Endpoints
For information regarding the various endpoints please see the postman documentation.

https://documenter.getpostman.com/view/3609222/RzZ1sPcW

### Docker

Docker support is part of release 1.0 but not currently tested.
