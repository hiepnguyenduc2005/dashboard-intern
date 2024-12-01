FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ARG API_KEY
ARG PASSWORD 
ARG SECRET

ENV WEBSITE "https://my.api.mockaroo.com"

ENV API_KEY $API_KEY
ENV PASSWORD $PASSWORD
ENV SECRET $SECRET

COPY . .

RUN pytest

CMD ["python", "app.py"]
