# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 5
# Experiment Memory System
# ============================================================
#
# PURPOSE:
#
# Every successful experiment receives a permanent ID:
#
#     EXP-0001
#     EXP-0002
#     EXP-0003
#     ...
#
# Each experiment saves:
#
# 1. Experiment result
# 2. Exact parameters used
# 3. Exact Python code used
# 4. Experiment ID
# 5. Commit SHA
# 6. East Africa Time (UTC+3)
#
# The leaderboard keeps the history of experiments.
#
# DUPLICATE PROTECTION:
#
# If parameters.json has not changed since the last experiment,
# the experiment is skipped unless FORCE_RERUN=true.
#
# ============================================================


import csv
import hashlib
import json
import os
import shutil

from datetime import datetime, timezone, timedelta
from pathlib import Path


print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 5")
print("=" * 70)


# ============================================================
# STEP 1
# LOAD PARAMETERS
# ============================================================

parameters_file = Path("parameters.json")


with parameters_file.open(
    "r",
    encoding="utf-8"
) as file:

    parameters = json.load(file)


# Create a fingerprint of the parameters.
#
# This lets us determine whether the parameters have changed
# since the previous experiment.

parameters_hash = hashlib.sha256(
    json.dumps(
        parameters,
        sort_keys=True
    ).encode("utf-8")
).hexdigest()


# ============================================================
# STEP 2
# LEADERBOARD SETTINGS
# ============================================================

leaderboard_file = Path("leaderboard.csv")


FIELDNAMES = [
    "experiment_id",
    "return_percent",
    "profit",
    "status",
    "parameters_hash",
    "commit_sha",
    "timestamp_eat",
]


# ============================================================
# STEP 3
# READ EXISTING EXPERIMENT HISTORY
# ============================================================

existing_rows = []


if leaderboard_file.exists():

    with leaderboard_file.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            # Only keep properly formed experiment rows.

            if row.get("experiment_id"):

                existing_rows.append(row)


# ============================================================
# STEP 4
# CHECK WHETHER PARAMETERS CHANGED
# ============================================================

force_rerun = (
    os.environ.get(
        "FORCE_RERUN",
        "false"
    ).strip().lower() == "true"
)


last_row = (
    existing_rows[-1]
    if existing_rows
    else None
)


last_hash = (
    last_row.get("parameters_hash")
    if last_row
    else None
)


if (
    last_hash == parameters_hash
    and not force_rerun
):

    print()

    print(
        "NO NEW EXPERIMENT CREATED."
    )

    print(
        "parameters.json is unchanged "
        "from the previous experiment."
    )

    if last_row:

        print(
            f"Previous experiment: "
            f"{last_row['experiment_id']}"
        )

    print()

    print(
        "Change parameters.json to create "
        "a new experiment."
    )

    print(
        "Alternatively use FORCE_RERUN=true."
    )

    print()

    raise SystemExit(0)


# ============================================================
# STEP 5
# CREATE EXPERIMENT ID
# ============================================================
#
# We deliberately use the simple numbering system:
#
# EXP-0001
# EXP-0002
# EXP-0003
#
# The number is based on the highest experiment number already
# recorded in leaderboard.csv.
#
# ============================================================


experiment_folder = Path("experiments")


experiment_folder.mkdir(
    exist_ok=True
)


highest_id = 0


for row in existing_rows:

    experiment_id_text = row.get(
        "experiment_id",
        ""
    ).strip()


    if experiment_id_text.startswith("EXP-"):

        try:

            number = int(
                experiment_id_text.replace(
                    "EXP-",
                    ""
                )
            )


            if number > highest_id:

                highest_id = number

        except ValueError:

            # Ignore malformed experiment IDs.

            pass


experiment_number = highest_id + 1


experiment_id = (
    f"EXP-{experiment_number:04d}"
)


# ============================================================
# STEP 6
# GET GITHUB INFORMATION
# ============================================================


commit_sha = os.environ.get(
    "GITHUB_SHA",
    "local"
)


# ============================================================
# STEP 7
# CREATE EAST AFRICA TIME
# ============================================================
#
# GitHub's computer normally works with UTC.
#
# Kenya / East Africa is UTC+3.
#
# We therefore calculate:
#
# UTC + 3 hours
#
# Example:
#
# 01:00 UTC
# becomes
# 04:00 EAT
#
# ============================================================


east_africa_timezone = timezone(
    timedelta(hours=3)
)


run_timestamp = (
    datetime.now(timezone.utc)
    .astimezone(east_africa_timezone)
    .strftime(
        "%Y-%m-%dT%H:%M:%S+03:00"
    )
)


print()

print("Experiment ID:")
print(experiment_id)

print()

print("Commit SHA:")
print(commit_sha)

print()

print("East Africa Time:")
print(run_timestamp)


# ============================================================
# STEP 8
# CREATE EXPERIMENT DIRECTORY
# ============================================================


current_experiment = (
    experiment_folder /
    experiment_id
)


current_experiment.mkdir(
    exist_ok=False
)


print()

print("Experiment folder created:")

print(current_experiment)


# ============================================================
# STEP 9
# RUN SIMPLE EXPERIMENT
# ============================================================
#
# THIS IS STILL OUR SIMPLE TEST STRATEGY.
#
# Later this section will become:
#
# VectorBT
#     ↓
# historical market data
#     ↓
# strategy
#     ↓
# backtest
#     ↓
# metrics
#
# Eventually an optimizer/AI system will modify the
# parameters and repeatedly run this section.
#
# ============================================================


capital = parameters[
    "starting_capital"
]


strategy_return = parameters[
    "strategy_return"
]


ending_capital = (
    capital *
    (1 + strategy_return)
)


profit = (
    ending_capital -
    capital
)


return_percent = (
    profit /
    capital
) * 100


# ============================================================
# STEP 10
# SAVE EXPERIMENT RESULT
# ============================================================


result_file = (
    current_experiment /
    "experiment_result.txt"
)


with result_file.open(
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "QUANT RESEARCH EXPERIMENT\n"
    )

    file.write(
        "=" * 70 +
        "\n"
    )

    file.write(
        f"Experiment ID: "
        f"{experiment_id}\n"
    )

    file.write(
        f"Commit SHA: "
        f"{commit_sha}\n"
    )

    file.write(
        f"Timestamp EAT: "
        f"{run_timestamp}\n"
    )

    file.write("\n")


    file.write(
        "PARAMETERS\n"
    )

    file.write(
        "-" * 70 +
        "\n"
    )


    for key, value in parameters.items():

        file.write(
            f"{key}: {value}\n"
        )


    file.write("\n")


    file.write(
        "RESULTS\n"
    )

    file.write(
        "-" * 70 +
        "\n"
    )


    file.write(
        f"Starting capital: "
        f"{capital}\n"
    )

    file.write(
        f"Ending capital: "
        f"{ending_capital}\n"
    )

    file.write(
        f"Profit: "
        f"{profit}\n"
    )

    file.write(
        f"Return: "
        f"{return_percent}%\n"
    )


# ============================================================
# STEP 11
# PRESERVE THE EXACT PARAMETERS
# ============================================================


shutil.copy(
    parameters_file,
    current_experiment /
    "parameters.json"
)


# ============================================================
# STEP 12
# PRESERVE THE EXACT PYTHON CODE
# ============================================================


shutil.copy(
    "hello.py",
    current_experiment /
    "hello.py"
)


# ============================================================
# STEP 13
# UPDATE LEADERBOARD
# ============================================================


new_row = {

    "experiment_id":
        experiment_id,

    "return_percent":
        round(
            return_percent,
            2
        ),

    "profit":
        round(
            profit,
            2
        ),

    "status":
        "completed",

    "parameters_hash":
        parameters_hash,

    "commit_sha":
        commit_sha,

    "timestamp_eat":
        run_timestamp,
}


existing_rows.append(
    new_row
)


# ============================================================
# STEP 14
# WRITE CLEAN LEADERBOARD
# ============================================================


with leaderboard_file.open(
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=FIELDNAMES
    )

    writer.writeheader()

    writer.writerows(
        existing_rows
    )


# ============================================================
# STEP 15
# DISPLAY RESULTS
# ============================================================


print()

print("=" * 70)

print("EXPERIMENT COMPLETE")

print("=" * 70)

print()

print(
    f"Experiment ID: "
    f"{experiment_id}"
)

print(
    f"Return: "
    f"{return_percent}%"
)

print(
    f"Profit: "
    f"{profit}"
)

print(
    f"Time: "
    f"{run_timestamp}"
)

print()

print("Saved:")

print(current_experiment)

print()

print("Leaderboard:")

print(leaderboard_file)

print()

print("=" * 70)
