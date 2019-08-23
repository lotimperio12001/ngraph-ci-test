"""Static page generator based on jinja2 templates API.

Jinja2 docs: https://jinja.palletsprojects.com/en/2.10.x/api/
"""

import csv
import json

from collections import OrderedDict
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


def _mark_coverage(percentage):
    """Return mark from A to F based on passed tests percentage.

    :param percentage: Percentage of passed unit tests.
    :type percentage: float
    :return: Mark from A to F.
    :rtype: str
    """
    mark_table = {
        "A": (90, 101),
        "B": (80, 90),
        "C": (70, 80),
        "D": (60, 70),
        "E": (50, 60),
        "F": (0, 50),
    }
    for mark, mark_range in mark_table.items():
        if int(percentage) in range(*mark_range):
            return mark


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
    coverage["mark"] = _mark_coverage(coverage["passed"])
    return coverage


def _load_ops_csv(path):
    ops_table = OrderedDict()
    with open(path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ops_table[row["Op"]] = row.get("None").replace("!", "").lower()
    return ops_table


def _load_report(path):
    dummy_report = {"failed": [], "passed": [], "skipped": []}
    try:
        with open(path, "r") as report_file:
            report = json.load(report_file)
            del report["date"]
    except (IOError, json.decoder.JSONDecodeError):
        report = dummy_report

    swapped_report = OrderedDict()
    for status, test_names in report.items():
        for test in test_names:
            swapped_report[test] = status

    swapped_report = OrderedDict(
        sorted(swapped_report.items(), key=lambda item: item[0])
    )
    return swapped_report


# Load Ops coverage table from csv file
onnxruntime_ops = _load_ops_csv("../results/onnx-runtime/stable/nodes.csv")
ngraph_ops = _load_ops_csv("../results/ngraph/development/nodes.csv")
tensorflow_ops = _load_ops_csv("../results/tensorflow/stable/nodes.csv")
pytorch_ops = _load_ops_csv("../results/pytorch/development/nodes.csv")

# Load report from json file
onnxruntime_report = _load_report("../results/onnx-runtime/stable/report.json")
ngraph_report = _load_report("../results/ngraph/development/report.json")
tensorflow_report = _load_report("../results/tensorflow/stable/report.json")
pytorch_report = _load_report("../results/pytorch/development/report.json")

# Load trend from json file
onnxruntime_trend = _load_trend("../results/onnx-runtime/stable/trend.json")
ngraph_trend = _load_trend("../results/ngraph/development/trend.json")
tensorflow_trend = _load_trend("../results/tensorflow/stable/trend.json")
pytorch_trend = _load_trend("../results/pytorch/development/trend.json")

# Calculate coverage percentages
onnxruntime_coverage = _get_coverage_percentage(onnxruntime_trend)
ngraph_coverage = _get_coverage_percentage(ngraph_trend)
tensorflow_coverage = _get_coverage_percentage(tensorflow_trend)
pytorch_coverage = _get_coverage_percentage(pytorch_trend)

# Prepare data for templates
database_stable = OrderedDict(
    {
        "onnxruntime": {
            "version": {"onnx": "1.5", "backend": "0.5.0"},
            "name": "ONNX-Runtime",
            "trend": onnxruntime_trend,
            "coverage": onnxruntime_coverage,
            "ops": onnxruntime_ops,
            "report": onnxruntime_report,
        },
        "ngraph": {
            "version": {"onnx": "1.5", "backend": "dev"},
            "name": "nGraph",
            "trend": ngraph_trend,
            "coverage": ngraph_coverage,
            "ops": ngraph_ops,
            "report": ngraph_report,
        },
        "tensorflow": {
            "version": {"onnx": "1.5", "backend": "1.14.0"},
            "name": "Tensorflow",
            "trend": tensorflow_trend,
            "coverage": tensorflow_coverage,
            "ops": tensorflow_ops,
            "report": tensorflow_report,
        },
        "pytorch": {
            "version": {"onnx": "1.5", "backend": "dev"},
            "name": "Pytorch",
            "trend": pytorch_trend,
            "coverage": pytorch_coverage,
            "ops": pytorch_ops,
            "report": pytorch_report,
        },
    }
)

database_dev = OrderedDict(
    {
        "onnxruntime": {
            "version": {"onnx": "1.5", "backend": "0.5.0"},
            "name": "ONNX-Runtime",
            "trend": onnxruntime_trend,
            "coverage": onnxruntime_coverage,
        },
        "ngraph": {
            "version": {"onnx": "1.5", "backend": "dev"},
            "name": "nGraph",
            "trend": ngraph_trend,
            "coverage": ngraph_coverage,
        },
        "tensorflow": {
            "version": {"onnx": "1.5", "backend": "1.14.0"},
            "name": "Tensorflow",
            "trend": tensorflow_trend,
            "coverage": tensorflow_coverage,
        },
        "pytorch": {
            "version": {"onnx": "1.5", "backend": "dev"},
            "name": "Pytorch",
            "trend": pytorch_trend,
            "coverage": pytorch_coverage,
        },
    }
)

# Sort data by score
database_stable = OrderedDict(
    sorted(
        database_stable.items(),
        key=lambda item: item[1]["coverage"]["passed"],
        reverse=True,
    )
)
database_dev = OrderedDict(
    sorted(
        database_dev.items(),
        key=lambda item: item[1]["coverage"]["passed"],
        reverse=True,
    )
)


# Website
# Create Jinja2 templates environment
env = Environment(
    loader=PackageLoader("templates-module", "templates"),
    autoescape=select_autoescape(["html"]),
)

# Generate static page
index_template = env.get_template("index.html")
index_static = index_template.render(
    database_dev=database_dev, database_stable=database_stable
)

# Save static page to file
with open("../index.html", "w") as f:
    f.write(index_static)
