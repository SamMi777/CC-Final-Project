FROM python:3.10-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY templates/ templates/
COPY static/frozenfour.png templates/frozenfour.png
CMD ["python", "accessories.py", "templates/frozenfour.png"]
