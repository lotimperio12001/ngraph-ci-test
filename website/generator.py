import json

from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


def _load_trend(path):
    dummy_trend =  [{
    "date": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
    "failed": 1,
    "passed": 0,
    "skipped": 0
    }]

    try:
        with open(path, "r") as trend_file:
                trend = json.load(trend_file)
    except (IOError, json.decoder.JSONDecodeError):
        trend = dummy_trend
    return trend

def _get_coverage_percentage(trend):
    coverage = {"total": (trend[-1].get("failed", 0) + trend[-1].get("passed", 0))}
    coverage["passed"] = trend[-1].get("passed", 0) / coverage.get("total", 1) * 100
    coverage["failed"] = trend[-1].get("failed", 0) / coverage.get("total", 1) * 100
    return coverage

# Load trend from file
onnxruntime_trend = _load_trend("../results/onnx-runtime/stable/trend.json")
ngraph_trend =  _load_trend("../results/ngraph/dev/trend.json")
tensorflow_trend = _load_trend("../results/tensorflow/stable/trend.json")
pytorch_trend = _load_trend("../results/pytorch/development/trend.json")

# Coverage percentages
onnxruntime_coverage = _get_coverage_percentage(onnxruntime_trend)
ngraph_coverage = _get_coverage_percentage(ngraph_trend)
tensorflow_coverage = _get_coverage_percentage(tensorflow_trend)
pytorch_coverage = _get_coverage_percentage(pytorch_trend)

# Jinja templates environment
env = Environment(
    loader=PackageLoader('templates-module', 'templates'),
    autoescape=select_autoescape(['html'])
)

scoreboard_data = {"onnxruntime":{"trend": onnxruntime_trend, "coverage":  onnxruntime_coverage}, \
    "ngraph": {"trend": ngraph_trend, "coverage":  ngraph_coverage},
    "tensorflow": {"trend": tensorflow_trend, "coverage":  tensorflow_coverage},
    "pytorch": {"trend": pytorch_trend, "coverage":  pytorch_coverage}}

index_template = env.get_template('index.html')
index_static = index_template.render(scoreboard_data)

with open("../index.html", "w") as f:
    f.write(index_static)
