# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 8
# ============================================================
#
# PURPOSE:
#
# Level 8 teaches the system to examine its own experiment
# history and identify the best experiment found so far.
#
# CURRENT ARCHITECTURE:
#
# parameters.json
#        |
#        v
# hello.py
#        |
#        v
# EXP-0001 / EXP-0002 / ...
#        |
#        v
# leaderboard.csv
#        |
#        v
# FIND BEST EXPERIMENT
#        |
#        v
# best_experiment.txt
#
#
# FUTURE:
#
# leaderboard.csv
#        |
#        v
# AI analysis
#        |
#        v
# improved parameters
#        |
#        v
# new experiment
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
print("QUANT RESEARCH EXPERIMENT — LEVEL 8")
print("=" * 70)


# ============================================================
# STEP 1
# LOAD PARAMETERS
# ============================================================

parameters_file = Path("parameters.json")


with parameters_file.open("r", encoding="utf-8") as file:
    parameters = json.load(file)


# Create a fingerprint of the parameters.
#
# This allows us to recognize whether the parameters changed.

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
    "timestamp_utc",
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

            if row.get("experiment_id"):

                existing_rows.append(row)


print()
print("Previous experiments found:")
print(len(existing_rows))


# ============================================================
# STEP 4
# PREVENT UNINTENTIONAL DUPLICATES
# ============================================================

force_rerun = (
    os.environ.get(
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
        "The parameters have not changed since the"
    )

    if last_row:

        print(
            f"last experiment ({last_row['experiment_id']})."
        )

    print()
    print(
        "Skipping this run to prevent an accidental duplicate."
    )

    print(
        "Use FORCE_RERUN=true when you deliberately want"
        " to repeat the experiment."
    )

    raise SystemExit(0)


# ============================================================
# STEP 5
# CREATE UNIQUE EXPERIMENT ID
# ============================================================
#
# We intentionally return to the simple EXP-0001 style.
#
# The ID is based on the existing experiment directories
# and leaderboard history.
#
# ============================================================

experiment_folder = Path("experiments")

experiment_folder.mkdir(
    exist_ok=True
)


highest_id = 0


# Check leaderboard history.

for row in existing_rows:

    experiment_id_value = row.get(
        "experiment_id",
        ""
    )

    if experiment_id_value.startswith("EXP-"):

        try:

            number = int(
                experiment_id_value.replace(
                    "EXP-",
                    ""
                )
            )

            highest_id = max(
                highest_id,
                number
            )

        except ValueError:

            pass


# Also check actual experiment folders.
#
# This protects us if the leaderboard was manually edited.

for folder in experiment_folder.iterdir():

    if folder.is_dir():

        folder_name = folder.name

        if folder_name.startswith("EXP-"):

            try:

                number = int(
                    folder_name.replace(
                        "EXP-",
                        ""
                    )
                )

                highest_id = max(
                    highest_id,
                    number
                )

            except ValueError:

                pass


experiment_number = highest_id + 1


experiment_id = (
    f"EXP-{experiment_number:04d}"
)


# ============================================================
# STEP 6
# CREATE TIMESTAMP
# ============================================================

commit_sha = os.environ.get(
    "GITHUB_SHA",
    "unknown"
)


utc_now = datetime.now(
    timezone.utc
)


east_africa_time = (
    utc_now
    + timedelta(hours=3)
)


timestamp_utc = utc_now.strftime(
    "%Y-%m-%dT%H:%M:%SZ"
)


timestamp_eat = east_africa_time.strftime(
    "%Y-%m-%dT%H:%M:%S+03:00"
)


print()
print("Experiment ID:")
print(experiment_id)

print()
print("Commit SHA:")
print(commit_sha)

print()
print("UTC:")
print(timestamp_utc)

print()
print("East Africa Time:")
print(timestamp_eat)


# ============================================================
# STEP 7
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
print("Experiment directory:")
print(current_experiment)


# ============================================================
# STEP 8
# RUN THE CURRENT EXPERIMENT
# ============================================================

capital = parameters[
    "starting_capital"
]


strategy_return = parameters[
    "strategy_return"
]


ending_capital = (
    capital
    * (1 + strategy_return)
)


profit = (
    ending_capital
    - capital
)


return_percent = (
    profit
    / capital
) * 100


print()
print("RESULT")
print("-" * 70)

print(
    f"Starting capital: {capital}"
)

print(
    f"Strategy return: {strategy_return}"
)

print(
    f"Profit: {profit}"
)

print(
    f"Return: {return_percent}%"
)


# ============================================================
# STEP 9
# SAVE COMPLETE EXPERIMENT REPORT
# ============================================================

result_file = (
    current_experiment
    / "experiment_result.txt"
)


with result_file.open(
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "QUANT RESEARCH EXPERIMENT\n"
    )

    file.write(
        "=" * 70
        + "\n"
    )

    file.write(
        f"Experiment ID: {experiment_id}\n"
    )

    file.write(
        f"Commit SHA: {commit_sha}\n"
    )

    file.write(
        f"Timestamp UTC: {timestamp_utc}\n"
    )

    file.write(
        f"Timestamp East Africa: {timestamp_eat}\n"
    )

    file.write("\n")

    file.write(
        "PARAMETERS\n"
    )

    file.write(
        "-" * 70
        + "\n"
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
        "-" * 70
        + "\n"
    )

    file.write(
        f"Starting capital: {capital}\n"
    )

    file.write(
        f"Ending capital: {ending_capital}\n"
    )

    file.write(
        f"Profit: {profit}\n"
    )

    file.write(
        f"Return: {return_percent}%\n"
    )


# ============================================================
# STEP 10
# PRESERVE THE CODE AND PARAMETERS
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


# ============================================================
# STEP 11
# ADD EXPERIMENT TO LEADERBOARD
# ============================================================

rows = list(existing_rows)


rows.append(
    {
        "experiment_id": experiment_id,

        "return_percent": round(
            return_percent,
            2
        ),

        "profit": round(
            profit,
            2
        ),

        "status": "completed",

        "parameters_hash":
            parameters_hash,

        "commit_sha":
            commit_sha,

        "timestamp_utc":
            timestamp_utc,
    }
)


# ============================================================
# STEP 12
# REWRITE CLEAN LEADERBOARD
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

    writer.writerows(rows)


print()
print("Leaderboard updated.")


# ============================================================
# STEP 13
# FIND THE BEST EXPERIMENT
# ============================================================
#
# THIS IS THE IMPORTANT NEW LEVEL 8 FEATURE.
#
# We now ask:
#
# "Among all completed experiments, which has the
# highest return?"
#
# ============================================================

completed_rows = []


for row in rows:

    if row.get("status") != "completed":

        continue

    try:

        row_return = float(
            row["return_percent"]
        )

        completed_rows.append(
            (row_return, row)
        )

    except (
        ValueError,
        TypeError
    ):

        continue


best_experiment_file = Path(
    "best_experiment.txt"
)


if completed_rows:

    # Highest return wins.

    best_return, best_row = max(
        completed_rows,
        key=lambda item: item[0]
    )


    best_id = best_row[
        "experiment_id"
    ]

    best_profit = best_row[
        "profit"
    ]


    print()
    print("=" * 70)
    print("CURRENT BEST EXPERIMENT")
    print("=" * 70)

    print()
    print(
        f"Experiment: {best_id}"
    )

    print(
        f"Return: {best_return}%"
    )

    print(
        f"Profit: {best_profit}"
    )


    # --------------------------------------------------------
    # SAVE BEST EXPERIMENT REPORT
    # --------------------------------------------------------

    with best_experiment_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "CURRENT BEST EXPERIMENT\n"
        )

        file.write(
            "=" * 70
            + "\n\n"
        )

        file.write(
            f"Experiment ID: {best_id}\n"
        )

        file.write(
            f"Return: {best_return}%\n"
        )

        file.write(
            f"Profit: {best_profit}\n"
        )

        file.write(
            f"Status: {best_row['status']}\n"
        )

        file.write(
            f"Parameters hash: "
            f"{best_row.get('parameters_hash', '')}\n"
        )

        file.write(
            f"Commit SHA: "
            f"{best_row.get('commit_sha', '')}\n"
        )

        file.write(
            f"Timestamp UTC: "
            f"{best_row.get('timestamp_utc', '')}\n"
        )

        file.write("\n")

        file.write(
            "This experiment currently has the highest"
            " recorded return in the leaderboard.\n"
        )


else:

    print()
    print(
        "No completed experiments were found."
    )


# ============================================================
# STEP 14
# FINISH
# ============================================================

print()
print("=" * 70)
print("LEVEL 8 EXPERIMENT COMPLETE")
print("=" * 70)

print()
print("Saved experiment:")
print(current_experiment)

print()
print("Leaderboard:")
print(leaderboard_file)

print()
print("Best experiment report:")
print(best_experiment_file)
