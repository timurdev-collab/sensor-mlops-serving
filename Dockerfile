FROM python:3.11-slim
WORKDIR /app
COPY service ./service
EXPOSE 8001
CMD ["python", "-m", "service.api"]
