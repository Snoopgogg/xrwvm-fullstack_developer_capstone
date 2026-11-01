# Run the Cars Dealership Capstone locally

## Prerequisites
- Docker Desktop or Docker Engine with the Compose plugin
- Git

## Start the full stack
From the `server` directory:

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f django
```

Open the application at:
- Django application: http://localhost:8000/
- Dealer API: http://localhost:3030/
- Sentiment API: http://localhost:5050/

## API smoke tests

```bash
curl http://localhost:8000/djangoapp/get_dealers
curl http://localhost:8000/djangoapp/get_dealers/Kansas
curl http://localhost:8000/djangoapp/dealer/1
curl http://localhost:8000/djangoapp/reviews/dealer/2
curl http://localhost:8000/djangoapp/get_cars
curl http://localhost:5050/analyze/Fantastic%20services
```

## IBM Cloud Code Engine deployment

Build and push three images to a registry accessible by your IBM Cloud Code Engine project:
1. `server/Dockerfile` (Django web application, port 8000)
2. `server/database/Dockerfile` (Node.js dealer API, port 3030)
3. `server/djangoapp/microservices/Dockerfile` (sentiment service, port 5050)

Create a MongoDB service reachable from Code Engine, then deploy the Node API and sentiment service first. Deploy Django last and configure these environment variables on the Django Code Engine application:
- `backend_url`: public/internal URL of the Node API
- `sentiment_analyzer_url`: public/internal URL of the sentiment service
- `PORT`: Code Engine assigned port (use 8000 if configured explicitly)

The final Q23 answer must be the actual public URL shown by Code Engine for the Django app. Do not use the GitHub repository URL, a localhost URL, or a placeholder in Q23.
