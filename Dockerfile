FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED="true"
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /bin/wait-for-it.sh \
      && chmod a+x /bin/wait-for-it.sh
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY consumer.py .