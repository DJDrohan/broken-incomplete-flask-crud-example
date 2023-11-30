FROM python:latest
WORKDIR /
COPY . .
RUN apt update && apt-get upgrade -y && apt-get install -y
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python","-m","flask","run"]