import json  # Unused import to trigger F401
import os
from datetime import datetime
from datetime import datetime as dt

import pytz
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)


def get_localized_times(utc_time: datetime) -> dict[str, str]:
    """
    Convert UTC time to various timezones

    ```
    Returns: Dict with keys: utc, europe, us_east, us_west, japan, taipei
        Values are ISO formatted strings with milliseconds
    ```
    """
    return {
        "utc": utc_time.isoformat(sep=" ", timespec="milliseconds"),
        "europe": utc_time.astimezone(pytz.timezone("Europe/London"))
        .isoformat(sep=" ", timespec="milliseconds")
        .replace("T", " "),
        "us_east": utc_time.astimezone(pytz.timezone("US/Eastern")).isoformat(
            sep=" ", timespec="milliseconds"
        ),
        "us_west": utc_time.astimezone(pytz.timezone("US/Pacific")).isoformat(
            sep=" ", timespec="milliseconds"
        ),
        "japan": utc_time.astimezone(pytz.timezone("Asia/Tokyo")).isoformat(
            sep=" ", timespec="seconds"
        ),
        "taipei": utc_time.astimezone(pytz.timezone("Asia/Taipei")).isoformat(
            sep=" ", timespec="milliseconds"
        ),
    }


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/process", methods=["GET"])
def process_timestamp() -> Response:
    utc_time = dt.now(pytz.UTC)
    times = get_localized_times(utc_time)

    return jsonify(
        {
            "utc_time": times["utc"],
            "europe_time": times["europe"],
            "us_east_time": times["us_east"],
            "us_west_time": times["us_west"],
            "japan_time": times["japan"],
            "taipei_time": times["taipei"],
            "request_count": request.args.get("count", "1"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
