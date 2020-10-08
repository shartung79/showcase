FROM python:3.8.6-alpine
RUN pip install -r requirements.txt
CMD ["python","app.py"]
COPY app.py /app.py
EXPOSE 5000
