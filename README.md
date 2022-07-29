# Cognitive
## Settings
### Create .env file 
```shell
cp /backend/.env_example /backend/.env
```
### Env Settings

```shell
# open .env
# vim
vim backend/.env
# or nano
nano backend/.env
# then generate key 
DATABASE_URL=postgres://root:root@db:5432/cognitive # database url
SECRET_KEY=    # SECRET KEY for  hashing passwords (to generate: openssl rand -hex 32 )
ALGORITHM=HS256 # manager pass hash algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=360  # lifetime of jwt token(for manager)
```
---
## How to start
### Install node modules on host machine 
```shell
cd frontend && npm install && cd ..
```
### Build containers
```shell
# docker compose v2
docker compose build
# or docker compose v1
docker-compose build
```
### Run docker compose
```shell
# v2
docker compose up
# or v1
docker-compose up
```
---
## Documentation
### [Backend](http://localhost:8000/docs)
```shell
http://localhost:8000/docs
```
### [Front](http://localhost:8080/)
```shell
http://localhost:8080/
```
