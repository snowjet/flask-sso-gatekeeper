FROM registry.access.redhat.com/ubi9/python-39

ENV PORT 8080
EXPOSE 8080
WORKDIR /usr/src/app

ADD . /usr/src/app/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/
CMD [ "gunicorn", "main:app", "--bind=0.0.0.0:8080"]
