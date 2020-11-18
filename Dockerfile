FROM python:3.9-slim

EXPOSE 5000
RUN mkdir -p /app/
WORKDIR /app/

COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install flask

#ENV FLASK_APP=app.py
#CMD ["flask", "run"]

COPY . /app
CMD ["python", "app.py"]