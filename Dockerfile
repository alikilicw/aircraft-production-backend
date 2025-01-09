FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/aircraft_backend

CMD python3 manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8001
