FROM python:3.8-alpine3.16
RUN pip install FLask
CMD ["python","app.py"]
COPY flask-app/app.py /app.py
EXPOSE 8080
