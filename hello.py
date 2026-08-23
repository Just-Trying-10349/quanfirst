# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 5 (FIXED v2)
# ============================================================
#
# WHY YOU GOT DUPLICATE-LOOKING ROWS:
# Your Actions history showed the workflow firing TWICE per change:
# once automatically on "push", and once from you manually clicking
# "Run workflow" a couple minutes later. Both runs used the exact
# same parameters.json, so both produced a "new" experiment with the
# same return/profit (and correctly unique IDs, since that part of
# the fix already worked).
#
# THE FIX (this file):
# Before creating a new experiment, we hash parameters.json and
# compare it to the hash stored on the LAST row of leaderboard.csv.
# If nothing changed, we skip creating a new experiment entirely —
# so re-running the workflow (on purpose or by accident) on unchanged
# parameters is a safe no-op instead of a duplicate entry.
#
# You can still force a rerun on unchanged parameters by setting the
# FORCE_RERUN environment variable to "true" (the fixed workflow
# exposes this as a workflow_dispatch input).
# ============================================================

import csv
import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 5 (FIXED v2)")
print("=" * 70)

# ------------------------------------------------------------
# STEP 1
# LOAD PARAMETERS
# ------------------------------------------------------------

parameters_file = Path("parameters.json")

with parameters_file.open("r", encoding="utf-8") as file:
    parameters = json.load(file)

# Hash of the parameters, order-independent, used for the
# skip-if-unchanged check below.
parameters_hash = hashlib.sha256(
    json.dumps(parameters, sort_keys=True).encode("utf-8")
).hexdigest()

# ------------------------------------------------------------
# STEP 2
# SKIP IF PARAMETERS HAVEN'T CHANGED SINCE THE LAST EXPERIMENT
# ------------------------------------------------------------

leaderboard_file = Path("leaderboard.csv")
force_rerun = os.environ.get("FORCE_RERUN", "false").strip().lower() == "true"

existing_rows = []
if leaderboard_file.exists():
    with leaderboard_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        existing_rows = [row for row in reader if row.get("experiment_id")]

last_row = existing_rows[-1] if existing_rows else None
last_hash = last_row.get("parameters_hash") if last_row else None

if last_hash == parameters_hash and not force_rerun:
    print()
    print("parameters.json is unchanged since the last recorded experiment")
    print(f"({last_row['experiment_id']}). Skipping to avoid a duplicate row.")
    print("Set FORCE_RERUN=true to run anyway.")
    raise SystemExit(0)

# ------------------------------------------------------------
# STEP 3
# CREATE A GUARANTEED-UNIQUE EXPERIMENT ID
# ------------------------------------------------------------
#
# GITHUB_RUN_ID is unique across every run of every workflow in this
# repo, forever, so two overlapping runs can never compute the same ID.

experiment_folder = Path("experiments")
experiment_folder.mkdir(exist_ok=True)

github_run_id = os.environ.get("GITHUB_RUN_ID")
github_run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")

if github_run_id:
    experiment_id = f"EXP-{github_run_id}-{github_run_attempt}"
else:
    experiment_id = f"EXP-LOCAL-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

print()
print("Experiment ID:")
print(experiment_id)

# ------------------------------------------------------------
# STEP 4
# CREATE EXPERIMENT DIRECTORY
# ------------------------------------------------------------

current_experiment = experiment_folder / experiment_id
current_experiment.mkdir(exist_ok=True)

print()
print("Experiment folder created:")
print(current_experiment)

# ------------------------------------------------------------
# STEP 5
# RUN SIMPLE EXPERIMENT
# ------------------------------------------------------------

capital = parameters["starting_capital"]
strategy_return = parameters["strategy_return"]

ending_capital = capital * (1 + strategy_return)
profit = ending_capital - capital
return_percent = (profit / capital) * 100

# ------------------------------------------------------------
# STEP 6
# SAVE RESULT
# ------------------------------------------------------------

result_file = current_experiment / "experiment_result.txt"

with result_file.open("w", encoding="utf-8") as file:
    file.write("QUANT RESEARCH EXPERIMENT\n")
    file.write("=" * 70 + "\n")
    file.write(f"Experiment ID: {experiment_id}\n")
    file.write(f"Time: {datetime.now()}\n\n")
    file.write("PARAMETERS\n")

    for key, value in parameters.items():
        file.write(f"{key}: {value}\n")

    file.write("\nRESULTS\n")
    file.write(f"Starting capital: {capital}\n")
    file.write(f"Ending capital: {ending_capital}\n")
    file.write(f"Profit: {profit}\n")
    file.write(f"Return: {return_percent}%\n")

# ------------------------------------------------------------
# STEP 7
# COPY IMPORTANT FILES
# ------------------------------------------------------------

shutil.copy("parameters.json", current_experiment / "parameters.json")
shutil.copy("hello.py", current_experiment / "hello.py")

# ------------------------------------------------------------
# STEP 8
# UPDATE LEADERBOARD
# ------------------------------------------------------------

rows = existing_rows
existing_ids = {row["experiment_id"] for row in rows}

if experiment_id not in existing_ids:
    rows.append(
        {
            "experiment_id": experiment_id,
            "return_percent": round(return_percent, 2),
            "profit": round(profit, 2),
            "status": "completed",
            "parameters_hash": parameters_hash,
        }
    )
else:
    print(f"WARNING: {experiment_id} already in leaderboard.csv, skipping append.")

with leaderboard_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "experiment_id",
            "return_percent",
            "profit",
            "status",
            "parameters_hash",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print()
print("Leaderboard updated:")
print(leaderboard_file)

# ------------------------------------------------------------
# FINISH
# ------------------------------------------------------------

print()
print("=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)
print()
print("Saved:")
print(current_experiment)
