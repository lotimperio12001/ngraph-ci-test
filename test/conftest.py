"""Implementation of hook functions for pytest.

Pytest calls hook functions to implement
initialization, running, test execution and reporting.
Each hook function name and its argument names need to match a hook specification.
All hooks have a pytest_ prefix.
From pytest docs: https://docs.pytest.org/en/latest/writing_plugins.html

We're implementing reporting hooks to collect data about
passing and failing tests for the scoreboard.
"""

import json
import os
import test

from datetime import datetime


# Keys for values to save in report (matched with terminalreporter.stats)
REPORT_KEYS = ["passed", "failed", "skipped"]


def pytest_addoption(parser):
    """Pytest hook function."""
    parser.addoption(
        "--onnx_backend",
        choices=[
            "ngraph_onnx.onnx_importer.backend",
            "onnxruntime.backend.backend",
            "onnx_tf.backend",
            "caffe2.python.onnx.backend",
        ],
        help="Select from available backends",
    )


def pytest_configure(pytest_config):
    """Pytest hook function."""
    onnx_backend_module = pytest_config.getvalue("onnx_backend")
    test.ONNX_BACKEND_MODULE = onnx_backend_module


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Pytest hook function."""
    # Set directories
    results_dir = os.environ.get("RESULTS_DIR", os.getcwd())
    version_dir = os.environ.get("VERSION_DIR", os.getcwd())

    # Collect and save the results
    report = _prepare_report(terminalreporter.stats)
    _save_report(report, results_dir)
    package_versions = _load_version(version_dir)
    scoreboard_config = _load_scoreboard_config("./config")
    core_package_versions = _filter_packages(package_versions, scoreboard_config)
    summary = _prepare_summary(report, core_package_versions)
    trend = _load_trend(results_dir)
    current_trend = _update_trend(summary, trend)
    _save_trend(current_trend, results_dir)


def _prepare_report(stats):
    """Return tests results report.

    Return results report based on pytest stats values
    that match keys listed in REPORT_KEYS.

    :param stats: _pytest.terminal.TerminalReporter.stats
    :type stats: dict
    :return: Dictionary with REPORT_KEYS and list of tests names as values.
    :rtype: dict
    """
    report = {"date": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
    for key in REPORT_KEYS:
        stats_group = stats.get(key, [])
        if not isinstance(stats_group, list):
            continue
        report[key] = []
        for record in stats_group:
            if hasattr(record, "nodeid"):
                # Remove file name from test id
                split_id = record.nodeid.split("::")
                clear_id = filter(lambda x: ".py" not in x, split_id)
                record_name = "::".join(clear_id)
                report[key].append(record_name)
        report[key].sort()
    return report


def _prepare_summary(report, package_versions=None):
    """Return tests summary including number of failed and passed tests.

    Return summary with length of each list in report.
    Summary example:
    {
        "date": "08/06/2019 09:37:45",
        "failed": 61,
        "passed": 497,
        "skipped": 0,
        "package_versions": [
            {
                "name": "onnx",
                "version": "1.5.0"
            },
            {
                "name": "onnxruntime",
                "version": "0.5.0"
            },
        ]
    }

    :param report: Dictionary with REPORT_KEYS and list of tests names as values.
    :type report: dict
    :return: Summary with length of each list in report.
    :rtype: dict
    """
    if not package_versions:
        package_versions = []

    summary = {"date": report.get("date", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))}
    summary["package_versions"] = package_versions
    for key in report.keys():
        if isinstance(report.get(key), list):
            summary[key] = len(report.get(key))
    return summary


def _save_report(report, results_dir, file_name="report.json"):
    """Save report data to the json file.

    :param report: Dictionary with REPORT_KEYS and list of tests names as values.
    :type report: dict
    :param results_dir: Path to direcotry with results.
    :type results_dir: str
    :param file_name: Name of report file, defaults to "report.json"
    :type file_name: str, optional
    """
    with open(os.path.join(results_dir, file_name), "w") as report_file:
        json.dump(report, report_file, sort_keys=True, indent=4)


def _save_trend(trend, results_dir, file_name="trend.json"):
    """Save trend data to the json file.

    Save trend data to the json file.
    Trend is a list of report summaries per date.
    This enable tracking number of failed and passed tests.
    Trend example:
    [
        {
            "date": "08/06/2019 09:37:45",
            "failed": 61,
            "passed": 497,
            "skipped": 0,
            "package_versions": [
                {
                    "name": "onnx",
                    "version": "1.5.0"
                }
            ]
        },
        {
            "date": "08/08/2019 08:34:18",
            "failed": 51,
            "passed": 507,
            "skipped": 0,
            "package_versions": [
                {
                    "name": "onnx",
                    "version": "1.6.0"
                }
            ]
        }
    ]

    :param trend: List of summaries.
    :type trend: list
    :param results_dir: Path to direcotry with results.
    :type results_dir: str
    :param file_name: Name of trend file, defaults to "trend.json"
    :type file_name: str, optional
    """
    with open(os.path.join(results_dir, file_name), "w") as trend_file:
        json.dump(trend, trend_file, sort_keys=True, indent=4)


def _load_trend(results_dir, file_name="trend.json"):
    """Load and return trend list from json file.

    Return list of summaries loaded from tests trend json file.
    If file is broken, empty or not found create and return new trend list.
    Trend is a list of report summaries per date.
    This enable tracking number of failed and passed tests.
    Trend example:
    [
        {
            "date": "08/06/2019 09:37:45",
            "failed": 61,
            "passed": 497,
            "skipped": 0,
            "package_versions": [
                {
                    "name": "onnx",
                    "pversion": "1.5.0"
                }
            ]
        },
        {
            "date": "08/08/2019 08:34:18",
            "failed": 51,
            "passed": 507,
            "skipped": 0,
            "package_versions": [
                {
                    "name": "onnx",
                    "version": "1.6.0"
                }
            ]
        }
    ]

    :param results_dir: Path to directory with results.
    :type results_dir: str
    :param file_name: Name of trend file, defaults to "trend.json".
    :type file_name: str, optional
    :return: List of summaries.
    :rtype: list
    """
    try:
        with open(os.path.join(results_dir, file_name), "r") as trend_file:
            trend = json.load(trend_file)
    except (IOError, json.decoder.JSONDecodeError):
        trend = []
    return trend


def _update_trend(summary, trend):
    """Return updated trend.

    Append result summary to the trend list if the last one result is
    different than current, otherwise replace last summary. Trend is a list of report
    summaries per date. This enable tracking number of failed and passed tests.
    Summary example:
    {
        "date": "08/06/2019 09:37:45",
        "failed": 61,
        "passed": 497,
        "skipped": 0,
        "package_versions": [
            {
                "name": "onnx",
                "version": "1.5.0"
            },
            {
                "name": "onnxruntime",
                "version": "0.5.0"
            },
        ]
    }
    Trend example:
    [
        {
            "date": "08/06/2019 09:37:45",
            "failed": 61,
            "passed": 497,
            "skipped": 0,
            "package_versions": [
                {
                    "name": "onnx",
                    "version": "1.5.0"
                }
            ]
        },
        {
            "date": "08/08/2019 08:34:18",
            "failed": 51,
            "passed": 507,
            "skipped": 0,
            "package_versions": [
                {
                    "name": "onnx",
                    "version": "1.6.0"
                }
            ]
        }
    ]

    :param summary: Contain length of each list in report.
    :type summary: dict
    :param trend: List of report summaries per date.
    :type trend: list
    :return: Updated trend.
    :rtype: list
    """
    # Trend should have at least two results
    valid_length = len(trend) >= 2 and summary.keys() == len(trend[-1].keys())
    equal_values = trend and all(
        summary.get(key) == trend[-1].get(key)
        for key in summary.keys()
        if key != "date"
    )
    # If the new result summary is the same as the last one in trend
    # then replace the old one to save current date,
    # otherwise append the new summary to the trend list
    if valid_length and equal_values:
        trend[-1] = summary
    else:
        trend.append(summary)
    return trend


def _load_version(version_dir, file_name="pip-list.json"):
    """Load and return python packages versions from json file.

    Use `pip list --format=json > pip-list.json` to generate and
    save installed python packages versions.
    Version example:
    [
        {
            "name": "onnx",
            "version": "1.5.0"
        },
        {
            "name": "onnxruntime",
            "version": "0.5.0"
        },
    ]

    :param version_dir: Directory of json file with pip list.
    :type version_dir: str
    :param file_name: Name of json file with pip list, defaults to "pip-list.json".
    :type file_name: str, optional
    :return: List of installed python packages names and versions.
    :rtype: list
    """
    try:
        with open(os.path.join(version_dir, file_name), "r") as version_file:
            package_versions = json.load(version_file)
    except (IOError, json.decoder.JSONDecodeError):
        package_versions = []
    return package_versions


def _filter_packages(package_versions, scoreboard_config):
    core_packages = ["onnx"]
    for state in ["stable", "development"]:
        core_packages += [
            framework_config.get("core_packages", [])
            for framework_key, framework_config in scoreboard_config.get(
                state, {}
            ).items()
        ]
    core_packages = [
        package for package in package_versions.keys() if package in core_packages
    ]
    return core_packages


def _load_scoreboard_config(file_path="./config.json"):
    file_path = os.path.abspath(file_path)
    try:
        with open(file_path, "r") as config_file:
            scoreboard_config = json.load(config_file)
    except (IOError, json.decoder.JSONDecodeError):
        scoreboard_config = {}
    return scoreboard_config
