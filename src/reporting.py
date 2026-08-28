import textwrap
from datetime import date, timedelta

from flask import Flask
from tabulate import tabulate

from src.data.blob import upload_file_to_blob
from src.data.queries import *

app = Flask(__name__)


@app.route("/report")
def generate_report():
    week = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    FILENAME = f"{week}-report.txt"

    with open(FILENAME, "w+") as f:
        f.write(f"=== Time Report — Week of {week} ===")

        f.write("\n\n")
        f.write("Per consultant:\n")
        f.write(
            textwrap.indent(
                tabulate(
                    weekly_report_consultants(), tablefmt="plain", numalign="right"
                ),
                "  ",
            )
        )

        f.write("\n\n")
        f.write("Per customer:\n")
        f.write(
            textwrap.indent(
                tabulate(weekly_report_companies(), tablefmt="plain", numalign="right"),
                "  ",
            )
        )

        f.write("\n\n")
        f.write(f"Total:\t{total_hours()}")

    upload_file_to_blob("reports", FILENAME, FILENAME)

    return ""
