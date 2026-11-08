from flask import Flask, jsonify, Response, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint']
)

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def record_metrics(response):
    if request.endpoint != 'metrics':
        duration = time.time() - g.start_time

        REQUEST_COUNT.labels(
            request.method,
            request.endpoint or 'unknown',
            response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            request.endpoint or 'unknown'
        ).observe(duration)

    return response

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to DevOps IC4 Project - Build 4",
        "status": "Running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/version")
def version():
    return jsonify({
        "version": "1.0",
        "project": "DevOps IC4"
    })

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
