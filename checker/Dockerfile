###########
# BUILDER #
###########

# pull official base image
FROM python:3.10.9-alpine3.17 as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# lint
RUN pip install --upgrade pip

COPY . .

# Install additional dependencies
RUN pip install requests
RUN pip install python-dotenv
RUN pip install python-telegram-bot

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
