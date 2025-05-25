FROM python:3.10-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY templates/ templates/
CMD ["python", "tournament.py"]

