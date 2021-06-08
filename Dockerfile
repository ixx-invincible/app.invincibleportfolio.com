FROM python:3.7

COPY ./requirements-prod.txt /.

RUN pip install -r requirements-prod.txt

EXPOSE 80

COPY ./app /app
COPY ./static /static

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
