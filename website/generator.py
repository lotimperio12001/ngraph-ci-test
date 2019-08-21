"""Static page generator based on jinja2 templates API.

Jinja2 docs: https://jinja.palletsprojects.com/en/2.10.x/api/
"""

import json

from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


def _load_trend(path):
    """Load and return trend list from json file.

    Return list of summaries loaded from tests trend json file.
    If file is broken, empty or not found then create and return new dummy trend.
    Trend is a list of report summaries per date.
    This enable tracking number of failed and passed tests.
    Trend example:
    [
        {
            "date": "08/06/2019 09:37:45",
            "failed": 61,
            "passed": 497,
            "skipped": 0
        },
        {
            "date": "08/08/2019 08:34:18",
            "failed": 51,
            "passed": 507,
            "skipped": 0
        }
    ]

    :param path: Path to file with results.
    :type path: str
    :return: List of summaries.
    :rtype: list
    """
    dummy_trend = [
        {
            "date": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
            "failed": 1,
            "passed": 0,
            "skipped": 0,
        }
    ]

    try:
        with open(path, "r") as trend_file:
            trend = json.load(trend_file)
    except (IOError, json.decoder.JSONDecodeError):
        trend = dummy_trend
    return trend


def _get_coverage_percentage(trend):
    """Create and return dict with passed and failed tests percentage.

    :param trend: Trend is a list of report summaries per date.
    :type trend: list
    :return: Dictionary with passed and failed tests percentage
    :rtype: dict
    """
    coverage = {"total": (trend[-1].get("failed", 0) + trend[-1].get("passed", 0))}
    coverage["passed"] = trend[-1].get("passed", 0) / coverage.get("total", 1) * 100
    coverage["failed"] = trend[-1].get("failed", 0) / coverage.get("total", 1) * 100
    return coverage


# Load trend from file
onnxruntime_trend = _load_trend("../results/onnx-runtime/stable/trend.json")
ngraph_trend = _load_trend("../results/ngraph/development/trend.json")
tensorflow_trend = _load_trend("../results/tensorflow/stable/trend.json")
pytorch_trend = _load_trend("../results/pytorch/development/trend.json")

# Calculate coverage percentages
onnxruntime_coverage = _get_coverage_percentage(onnxruntime_trend)
ngraph_coverage = _get_coverage_percentage(ngraph_trend)
tensorflow_coverage = _get_coverage_percentage(tensorflow_trend)
pytorch_coverage = _get_coverage_percentage(pytorch_trend)

# Create Jinja2 templates environment
env = Environment(
    loader=PackageLoader("templates-module", "templates"),
    autoescape=select_autoescape(["html"]),
)

# Prepare data for templates
scoreboard_data = {
    "onnxruntime": {"name": "ONNX-Runtime", "trend": onnxruntime_trend, "coverage": onnxruntime_coverage},
    "ngraph": {"name": "nGraph", "trend": ngraph_trend, "coverage": ngraph_coverage},
    "tensorflow": {"name": "Tensorflow", "trend": tensorflow_trend, "coverage": tensorflow_coverage},
    "pytorch": {"name": "Pytorch", "trend": pytorch_trend, "coverage": pytorch_coverage},
}

# Generate static page
index_template = env.get_template("index.html")
index_static = index_template.render(scoreboard_data)

# Save static page to file
with open("../index.html", "w") as f:
    f.write(index_static)
