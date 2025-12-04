# Tudo

## Introduction

Tudo is a simple todo application which is used to highlight the simplicity of building a full-stack application
when you keep the scope lean and reduce your pre-optimization

## How to run

Our Python REST service has a Dockerfile which allows us to easily run our application via the following command
```
docker-compose up --build
```

This will start our REST service which is accesible via localhost:8000

Frontend:
To run our simple HTMX frontend you can simply run a python web server via the following command

```bash
python -m http.server 8080

```
