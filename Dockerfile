FROM python:3.7
WORKDIR /code
ENV FLASK_APP=config.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
COPY requirements.txt requirements.txt
RUN apt-get install libpq-dev
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]