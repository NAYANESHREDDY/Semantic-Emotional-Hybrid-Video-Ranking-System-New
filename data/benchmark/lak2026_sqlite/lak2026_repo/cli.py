import json
import os
import sys
import time

# suppress warning from pydantic
from datetime import datetime, timedelta
from pathlib import Path

import click
from dotenv import load_dotenv
from loguru import logger

from cli_pak.dataops import commands as dataops
from cli_pak.vis import commands as vis
from cli_pak.metric import command as metric


def log_command(log_file: Path, command: str, start_time: float, end_time: float):
    if not log_file.exists():
        log_file.touch()
        # write {}
        log_file.write_text("{}")
    with open(log_file, "r") as f:
        log_data = json.load(f)
    duration = end_time - start_time
    # convert duration to hours, minutes, seconds using datetime
    duration_td = timedelta(seconds=duration)
    counter = len(log_data) + 1
    duration_dt = datetime.min + duration_td
    duration_str = duration_dt.strftime("%H:%M:%S")
    log_data[counter] = {
        "command": command,
        "duration": duration_str,
        "total_time_seconds": duration_td.total_seconds(),
        "timestamp": datetime.now().isoformat(),
    }
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)


@click.group()
@click.option(
    "--debug", is_flag=True, show_default=True, default=False, help="debug mode"
)
@click.option(
    "-v",
    "--log-level",
    default="DEBUG",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="log level",
)
def cli(debug, log_level):
    logger.remove()
    logger.add(sys.stderr, level=log_level)

    if debug:
        logger.add("debug.log", level="DEBUG", rotation="1 week", compression="zip")
        os.environ["LITELLM_LOG"] = "DEBUG"
        # litellm.set_verbose = True
    logger.add("error.log", level="ERROR", rotation="1 week", compression="zip")


cli.add_command(dataops.dataops)
cli.add_command(vis.vis)
cli.add_command(metric.metric)
if __name__ == "__main__":
    #  How can I catch ctrl+c and exit gracefully?

    log_file = Path("command_log.json")
    start = time.monotonic()
    try:
        load_dotenv()
        cli()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting gracefully.")
        sys.exit(0)
    finally:
        end = time.monotonic()
        # capture the passed command to click
        command = sys.argv[1]
        command_str = " ".join(sys.argv[1:])
        log_command(log_file, command_str, start, end)
