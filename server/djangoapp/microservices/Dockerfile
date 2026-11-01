FROM python:3.11-slim
WORKDIR /app
ENV PORT=5050
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["sh", "-c", "flask --app app run --host=0.0.0.0 --port=${PORT:-5050}"]
