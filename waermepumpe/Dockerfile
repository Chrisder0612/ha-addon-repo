FROM python:3.11-alpine

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .
COPY templates/ templates/
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
