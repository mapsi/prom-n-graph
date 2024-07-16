from flask import Flask, Response
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Enable default metrics
metrics.info('app_info', 'Application info', version='1.0.0')

# Custom counter metric
http_requests_total = metrics.counter(
    'http_requests_total', 'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.after_request
def after_request(response):
    http_requests_total.labels(
        method=request.method,
        endpoint=request.path,
        status_code=response.status_code
    ).inc()
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
