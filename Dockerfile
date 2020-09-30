FROM python:3.8.6-alpine
RUN pip install flask
CMD ["python","app.py"]
COPY app.py /app.py
