FROM python:3-alpine
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD python3 load_database_data.py && python3 -m flask run --host=0.0.0.0