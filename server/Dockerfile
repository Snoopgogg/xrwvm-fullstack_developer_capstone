FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --run-syncdb --noinput && python manage.py shell -c 'from djangoapp.populate import initiate; print(initiate())' && exec gunicorn djangoproj.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
