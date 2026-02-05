FROM python:3.9-slim
RUN pip install psycopg2-binary
COPY simulateur.py .
CMD ["python", "-u", "simulateur.py"]