FROM python:3.8.6-alpine
RUN pip install FLask
CMD ["python","app.py"]
COPY flask-app/app.py /app.py
EXPOSE 8080
