# Sensor MLOps Serving

A containerized Python inference-style API for industrial sensor anomaly flags.

## Features
- `POST /predict` validates sensor readings and returns anomaly indicators.
- Versioned rules with explainable anomaly reasons.
- `GET /health` and Prometheus-compatible `GET /metrics`.
- Structured request logging, Dockerfile, unit tests and CI.

**Scope:** This is a rules-based serving prototype, not a trained machine learning model. The project demonstrates API, observability and deployment foundations; model registry, live model training and cloud deployments are future work.

## Run locally
Python 3.10+; no third-party dependencies.

```bash
python -m service.api
curl -X POST http://localhost:8001/predict -H "Content-Type: application/json" -d '{"pressure_bar":2.0,"flow_lpm":60,"temperature_c":25}'
curl http://localhost:8001/metrics
python -m unittest discover -s tests -v
```

## Docker
```bash
docker build -t sensor-mlops-serving .
docker run --rm -p 8001:8001 sensor-mlops-serving
```

## API contract and smoke tests
Run `python -m unittest discover -s tests -v` for model and live-loopback HTTP tests, including malformed input behavior and metrics. Start the API with `python -m service.api` and then run `python scripts/smoke_test.py` in a second terminal. The [architecture](docs/architecture.md) distinguishes implemented rules-based serving from future trained-model infrastructure. No cloud deployment is claimed.

## AWS + Jira Cloud planning

See [AWS architecture and Jira Cloud backlog](docs/AWS_JIRA_ROADMAP.md). These are planning resources, **not** a claim of live AWS infrastructure or an active Jira Cloud board.
