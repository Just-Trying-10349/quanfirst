# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 7
# ============================================================
#
# PURPOSE:
#
# Level 7 teaches our research system to automatically identify
# the best experiment performed so far.
#
#
# CURRENT ARCHITECTURE:
#
# parameters.json
#       |
#       v
#     hello.py
#       |
#       v
#   EXP-0001
#       |
#       v
# experiment result
#       |
#       v
# leaderboard.csv
#       |
#       v
# compare experiments
#       |
#       v
# best_experiment.json
#
#
# IMPORTANT:
#
# We are NOT using AI yet.
#
# Python performs the comparison deterministically.
#
# Later, an external AI API can read:
#
#     leaderboard.csv
#     best_experiment.json
#     experiments/
#
# and help decide what should be tested next.
#
# ============================================================


import csv
import hashlib
import json
import os
import re
import shutil

from datetime import datetime, timezone, timedelta
from pathlib import Path


print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 7")
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


print()
print("Parameters loaded successfully.")


# ============================================================
# STEP 2
# CREATE PARAMETERS HASH
# ============================================================
#
# The hash gives every parameter configuration a fingerprint.
#
# Example:
#
# parameters A -> abc123...
# parameters B -> 72fd91...
#
# This will become useful later when we automatically search
# parameter combinations.
#
# ============================================================

parameters_hash = hashlib.sha256(
    json.dumps(
        parameters,
        sort_keys=True
    ).encode("utf-8")
).hexdigest()


print()
print("Parameters hash:")
print(parameters_hash)


# ============================================================
# STEP 3
# LOAD EXISTING LEADERBOARD
# ============================================================

leaderboard_file = Path(
    "leaderboard.csv"
)


FIELDNAMES = [
    "experiment_id",
    "return_percent",
    "profit",
    "status",
    "parameters_hash",
    "commit_sha",
    "timestamp_eat",
]


existing_rows = []


if leaderboard_file.exists():

    with leaderboard_file.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row.get("experiment_id"):

                existing_rows.append(row)


print()
print("Existing experiments:")
print(len(existing_rows))


# ============================================================
# STEP 4
# PREVENT ACCIDENTAL DUPLICATE EXPERIMENTS
# ============================================================

force_rerun = (
    os.environ
    .get(
        "FORCE_RERUN",
        "false"
    )
    .strip()
    .lower()
    == "true"
)


last_row = (
    existing_rows[-1]
    if existing_rows
    else None
)


last_hash = (
    last_row.get(
        "parameters_hash"
    )
    if last_row
    else None
)


if (
    last_hash == parameters_hash
    and not force_rerun
):

    print()
    print("=" * 70)
    print("DUPLICATE PARAMETERS DETECTED")
    print("=" * 70)

    print()

    print(
        "The current parameters were already used by:"
    )

    print(
        last_row["experiment_id"]
    )

    print()

    print(
        "No new experiment was created."
    )

    print()

    print(
        "Use FORCE_RERUN=true if you deliberately "
        "want to repeat the experiment."
    )

    print()

    raise SystemExit(0)


# ============================================================
# STEP 5
# CREATE EXPERIMENT DIRECTORY
# ============================================================

experiment_folder = Path(
    "experiments"
)


experiment_folder.mkdir(
    exist_ok=True
)


# ============================================================
# STEP 6
# FIND HIGHEST EXISTING EXPERIMENT NUMBER
# ============================================================
#
# We deliberately use the folders rather than leaderboard.csv.
#
# This prevents manually deleting a CSV row from causing an
# old experiment number to be reused.
#
# Example:
#
# EXP-0001
# EXP-0002
# EXP-0007
#
# Next experiment:
#
# EXP-0008
#
# ============================================================

highest_experiment_number = 0


experiment_pattern = re.compile(
    r"^EXP-(\d+)$"
)


for item in experiment_folder.iterdir():

    if not item.is_dir():

        continue


    match = experiment_pattern.match(
        item.name
    )


    if match:

        number = int(
            match.group(1)
        )


        if number > highest_experiment_number:

            highest_experiment_number = number


# ============================================================
# STEP 7
# CREATE NEW EXPERIMENT ID
# ============================================================

experiment_number = (
    highest_experiment_number + 1
)


experiment_id = (
    f"EXP-{experiment_number:04d}"
)


print()
print("New Experiment ID:")
print(experiment_id)


# ============================================================
# STEP 8
# GET GITHUB INFORMATION
# ============================================================

commit_sha = os.environ.get(
    "GITHUB_SHA",
    "local"
)


github_run_id = os.environ.get(
    "GITHUB_RUN_ID",
    "local"
)


print()
print("Commit SHA:")
print(commit_sha)


print()
print("GitHub Run ID:")
print(github_run_id)


# ============================================================
# STEP 9
# CREATE EAST AFRICA TIME
# ============================================================
#
# Kenya / East Africa uses UTC+3.
#
# GitHub's runner itself uses UTC.
#
# Therefore we explicitly create UTC+3 rather than relying
# on the computer's local timezone.
#
# ============================================================

east_africa_timezone = timezone(
    timedelta(hours=3)
)


run_timestamp = datetime.now(
    east_africa_timezone
).strftime(
    "%Y-%m-%dT%H:%M:%S%z"
)


print()
print("East Africa Time:")
print(run_timestamp)


# ============================================================
# STEP 10
# CREATE EXPERIMENT FOLDER
# ============================================================

current_experiment = (
    experiment_folder /
    experiment_id
)


# Safety check.
#
# Never overwrite an existing experiment.

if current_experiment.exists():

    raise RuntimeError(
        f"SAFETY ERROR: "
        f"{current_experiment} already exists. "
        f"Existing experiment will NOT be overwritten."
    )


current_experiment.mkdir()


print()
print("Experiment folder created:")
print(current_experiment)


# ============================================================
# STEP 11
# RUN THE CURRENT EXPERIMENT
# ============================================================
#
# This is still our deliberately simple mathematical
# experiment.
#
# We are NOT introducing VectorBT yet.
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


print()
print("Experiment result:")
print(
    f"Return: {return_percent}%"
)

print(
    f"Profit: {profit}"
)


# ============================================================
# STEP 12
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
        f"GitHub Run ID: "
        f"{github_run_id}\n"
    )

    file.write(
        f"Commit SHA: "
        f"{commit_sha}\n"
    )

    file.write(
        f"East Africa Time: "
        f"{run_timestamp}\n\n"
    )


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
# STEP 13
# PRESERVE THE EXACT EXPERIMENT INPUTS
# ============================================================

shutil.copy(
    "parameters.json",
    current_experiment /
    "parameters.json"
)


shutil.copy(
    "hello.py",
    current_experiment /
    "hello.py"
)


print()
print("Experiment files saved.")


# ============================================================
# STEP 14
# UPDATE LEADERBOARD
# ============================================================

rows = existing_rows.copy()


rows.append(
    {
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
)


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

    writer.writerows(rows)


print()
print("Leaderboard updated.")


# ============================================================
# STEP 15
# LEVEL 7 — FIND THE BEST EXPERIMENT
# ============================================================
#
# For now our only objective is:
#
#     HIGHEST RETURN
#
# Later we will replace this with a much more sophisticated
# objective involving things such as:
#
#     Sharpe ratio
#     Maximum drawdown
#     volatility
#     win rate
#     profit factor
#     number of trades
#
# ============================================================

print()
print("=" * 70)
print("LEVEL 7 — SEARCHING FOR CURRENT BEST EXPERIMENT")
print("=" * 70)


best_experiment = None


for row in rows:

    try:

        current_return = float(
            row["return_percent"]
        )

    except (
        ValueError,
        TypeError
    ):

        continue


    if best_experiment is None:

        best_experiment = row

    else:

        best_return = float(
            best_experiment[
                "return_percent"
            ]
        )


        if current_return > best_return:

            best_experiment = row


# ============================================================
# STEP 16
# SAVE BEST EXPERIMENT
# ============================================================

best_file = Path(
    "best_experiment.json"
)


if best_experiment is not None:

    with best_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            best_experiment,
            file,
            indent=4
        )


    print()
    print("CURRENT RESEARCH CHAMPION")
    print("-" * 70)

    print(
        f"Experiment ID: "
        f"{best_experiment['experiment_id']}"
    )

    print(
        f"Return: "
        f"{best_experiment['return_percent']}%"
    )

    print(
        f"Profit: "
        f"{best_experiment['profit']}"
    )

    print()

    print(
        "Champion saved to:"
    )

    print(
        "best_experiment.json"
    )


else:

    print()
    print(
        "WARNING: No valid experiments found."
    )


# ============================================================
# STEP 17
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("LEVEL 7 EXPERIMENT COMPLETE")
print("=" * 70)

print()

print(
    f"Experiment ID: {experiment_id}"
)

print(
    f"Return: {return_percent}%"
)

print(
    f"Profit: {profit}"
)

print(
    f"East Africa Time: {run_timestamp}"
)

print()

print(
    "Experiment saved:"
)

print(
    current_experiment
)

print()

if best_experiment is not None:

    print(
        "Current champion:"
    )

    print(
        best_experiment[
            "experiment_id"
        ]
    )

print()

print("=" * 70)
