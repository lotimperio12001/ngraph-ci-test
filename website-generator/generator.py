# ******************************************************************************
# Copyright 2017-2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

"""Static page generator based on jinja2 templates API.
Jinja2 docs: https://jinja.palletsprojects.com/en/2.10.x/api/
"""

import csv
import json
import os
import shutil

from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


def load_trend(file_dir, file_name="trend.json"):
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
            "skipped": 0,
            "versions": [
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
            "versions": [
                {
                    "name": "onnx",
                    "version": "1.6.0"
                }
            ]
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
            "failed": 0,
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


def mark_coverage(percentage):
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
        "F": (0, 59),
    }
    for mark, mark_range in mark_table.items():
        if int(percentage) in range(*mark_range):
            return mark


def get_coverage_percentage(trend):
    """Create and return dict with passed and failed tests percentage.

    :param trend: Trend is a list of report summaries per date.
    :type trend: list
    :return: Dictionary with passed and failed tests percentage
    :rtype: dict
    """
    coverage = {"total": (trend[-1].get("failed", 0) + trend[-1].get("passed", 0))}
    try:
        coverage["passed"] = trend[-1].get("passed", 0) / coverage.get("total", 0) * 100
        coverage["failed"] = trend[-1].get("failed", 0) / coverage.get("total", 0) * 100
    except ZeroDivisionError:
        coverage["passed"] = 0
        coverage["failed"] = 0
    coverage["mark"] = mark_coverage(coverage["passed"])
    return coverage


def load_ops_csv(file_dir, file_name="nodes.csv"):
    ops_table = OrderedDict()
    try:
        with open(os.path.join(file_dir, file_name), newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                ops_table[row["Op"]] = row.get("None").replace("!", "").lower()
    except IOError:
        pass  # Return empty dict
    return ops_table


def load_report(file_dir, file_name="report.json"):
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


def load_config(file_path):
    file_path = os.path.abspath(file_path)
    try:
        with open(file_path, "r") as config_file:
            config = json.load(config_file)
    except (IOError, json.decoder.JSONDecodeError) as err:
        raise IOError("Can't load config file !", err)
    return config


def prepare_database(config, state="stable"):
    config = config.get(state, {})
    database = OrderedDict()

    for framework_name, framework_config in config.items():
        results_dir = framework_config.get("results_dir")
        name = framework_config.get("name", framework_name)
        trend = load_trend(results_dir)
        versions = trend[-1].get("versions", [])
        coverage = get_coverage_percentage(trend)
        ops = load_ops_csv(results_dir)
        report = load_report(results_dir)

        database[framework_name] = {
            "name": name,
            "versions": versions,
            "trend": trend,
            "coverage": coverage,
            "ops": ops,
            "report": report,
        }

    database = sort_by_score(database)
    return database


def generate_page(template, output_dir, name, **template_args):
    page = template.render(template_args)

    # Save static page to file
    with open(os.path.join(output_dir, name), "w") as f:
        f.write(page)


def generate_pages(template, database, suffix):
    for framework, _ in database.items():
        framework_data = OrderedDict({framework: database.get(framework)})
        output_name = "{name}_{suffix}".format(name=framework, suffix=suffix)
        generate_page(
            template,
            deploy_paths.get("subpages", "./"),
            output_name,
            framework_data=framework_data,
        )


def sort_by_score(database):
    database = OrderedDict(
        sorted(
            database.items(),
            key=lambda item: item[1]["coverage"]["passed"],
            reverse=True,
        )
    )
    return database


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        dest="config",
        help="Load configuration from the specified json file",
        type=str,
    )
    args = parser.parse_args()

    # Load configuration from file
    config = load_config(args.config)
    deploy_paths = config.get("deploy_paths")

    # Prepare data for templates
    database_stable = prepare_database(config, state="stable")
    database_dev = prepare_database(config, state="development")

    # Website
    # Create Jinja2 templates environment
    env = Environment(
        loader=PackageLoader("templates-module", "templates"),
        autoescape=select_autoescape(["html"]),
    )

    # Create index.html file
    template = env.get_template("index.html")
    generate_page(
        template,
        deploy_paths.get("index", "./"),
        "index.html",
        database=database_stable,
    )

    # Create dev subpage
    template = env.get_template("index.html")
    generate_page(
        template,
        deploy_paths.get("subpages", "./"),
        "index_dev.html",
        database=database_dev,
        dev=True,
    )

    # Create details page for each framework
    template = env.get_template("details.html")
    generate_pages(template, database_stable, "details_stable.html")
    generate_pages(template, database_dev, "details_dev.html")

    # Copy resources to deploy dir
    # shutil.copytree function raises error if destination path exists
    resources_path = os.path.abspath("./website-generator/resources")
    deploy_resources_path = os.path.abspath(
        deploy_paths.get("resources", "./docs/resources")
    )
    if os.path.exists(deploy_resources_path):
        shutil.rmtree(deploy_resources_path)
    shutil.copytree(resources_path, deploy_resources_path)
