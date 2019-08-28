"""Static page generator based on jinja2 templates API.

Jinja2 docs: https://jinja.palletsprojects.com/en/2.10.x/api/
"""

import csv
import json
import os

from collections import OrderedDict
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


def _load_trend(file_dir, file_name="trend.json"):
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

    :param file_dir: Path to dir with trend file.
    :type path: str
    :param file_name: Name of trend file.
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
        with open(os.path.join(file_dir, file_name), "r") as trend_file:
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


def _load_ops_csv(file_dir, file_name="nodes.csv"):
    ops_table = OrderedDict()
    with open(os.path.join(file_dir, file_name), newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ops_table[row["Op"]] = row.get("None").replace("!", "").lower()
    return ops_table


def _load_report(file_dir, file_name="report.json"):
    dummy_report = {"failed": [], "passed": [], "skipped": []}
    try:
        with open(os.path.join(file_dir, file_name), "r") as report_file:
            report = json.load(report_file)
            del report["date"]
    except (IOError, json.decoder.JSONDecodeError):
        report = dummy_report

    # Swap value with keys to easier displaying data
    swapped_report = OrderedDict()
    for status, test_names in report.items():
        for test in test_names:
            swapped_report[test] = status

    swapped_report = OrderedDict(
        sorted(swapped_report.items(), key=lambda item: item[0])
    )
    return swapped_report


def _load_config(file_dir="./", file_name="config.json"):
    try:
        with open(os.path.join(file_dir, file_name), "r") as config_file:
            config = json.load(config_file)
    except (IOError, json.decoder.JSONDecodeError) as err:
        raise IOError("Can't load config file !", err)
    return config


def _prepare_database(state="stable"):
    config = _load_config()
    config = config[state]

    database = OrderedDict()
    for framework, conf in config.items():
        results_dir = conf.get("results_dir")
        name = conf.get("name", framework)
        trend = _load_trend(results_dir)
        version = _get_version(conf, trend)
        coverage = _get_coverage_percentage(trend)
        ops = _load_ops_csv(results_dir)
        report = _load_report(results_dir)

        database[framework] = {
            "name": name,
            "version": version,
            "trend": trend,
            "coverage": coverage,
            "ops": ops,
            "report": report,
        }
    return database


def _get_version(conf, trend):
    core_packages = conf.get("core_packages")
    packages_version = trend[-1].get("version")
    if core_packages and packages_version:
        version = [
            package
            for package in packages_version
            if package.get("name") in core_packages
        ]
        return version
    return []


# Prepare data for templates
database_stable = _prepare_database(state="stable")
database_dev = _prepare_database(state="development")

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
