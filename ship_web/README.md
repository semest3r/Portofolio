# SHIP WEB

## Create Virtual Environment
    pythone -m venv env

## install requirement
    pip install -r requirements.txt

## Set Database
    create file ".env"
    
    DATABASE_ENGINE=
    DATABASE_HOSTNAME=
    DATABASE_PORT=
    DATABASE_PASSWORD=
    DATABASE_NAME=
    DATABASE_USERNAME=
    SECRET_KEY=
    ALGORITHM=
    ACCESS_TOKEN_EXPIRE_MINUTES=

## RUN UVICORN
    uvicorn ship_web.main:app