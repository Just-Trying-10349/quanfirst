# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 5 (FIXED)
# ============================================================
#
# FIX SUMMARY (why your leaderboard could get duplicate/lost rows):
#
# 1. The old script picked the next experiment_id by COUNTING rows
#    in leaderboard.csv. If two workflow runs overlap (two pushes in
#    quick succession, or a manual run while a push-triggered run is
#    still going), both runs read the SAME leaderboard state and both
#    compute the SAME next ID. Whichever pushes second either fails
#    or clobbers the other.
#
# 2. current_experiment.mkdir() had no exist_ok=True, so an ID
#    collision would hard-crash the job instead of failing gracefully.
#
# 3. There was no retry/pull before "git push", so if the remote had
#    moved on (another run committed first), the push was rejected
#    and that run's leaderboard row was silently lost.
#
# THE FIX:
# Instead of deriving the ID from file state that can race, we derive
# it from GITHUB_RUN_ID — a number GitHub itself guarantees is unique
# across every run of every workflow in the repo, forever. No two
# runs can ever compute the same experiment_id, even if they run at
# the exact same second. When running locally (no GITHUB_RUN_ID env
# var), we fall back to a timestamp-based ID so the script still works
# on your laptop.
#
# ============================================================

import csv
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 5 (FIXED)")
print("=" * 70)

# ------------------------------------------------------------
# STEP 1
# LOAD PARAMETERS
# ------------------------------------------------------------

parameters_file = Path("parameters.json")

with parameters_file.open("r", encoding="utf-8") as file:
    parameters = json.load(file)

# ------------------------------------------------------------
# STEP 2
# CREATE A GUARANTEED-UNIQUE EXPERIMENT ID
# ------------------------------------------------------------
#
# GITHUB_RUN_ID is set automatically by GitHub Actions and is unique
# across every run of every workflow in this repository, forever.
# This means the ID no longer depends on reading leaderboard.csv,
# so two overlapping runs can NEVER collide.

experiment_folder = Path("experiments")
experiment_folder.mkdir(exist_ok=True)

github_run_id = os.environ.get("GITHUB_RUN_ID")
github_run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")

if github_run_id:
    # Running inside GitHub Actions -> guaranteed unique, no races possible.
    experiment_id = f"EXP-{github_run_id}-{github_run_attempt}"
else:
    # Running locally -> fall back to a timestamp so it still works,
    # but this branch is never used in CI.
    experiment_id = f"EXP-LOCAL-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

print()
print("Experiment ID:")
print(experiment_id)

# ------------------------------------------------------------
# STEP 3
# CREATE EXPERIMENT DIRECTORY
# ------------------------------------------------------------

current_experiment = experiment_folder / experiment_id

# exist_ok=True: even though a collision is now practically impossible,
# this makes the script gracefully idempotent instead of crashing.
current_experiment.mkdir(exist_ok=True)

print()
print("Experiment folder created:")
print(current_experiment)

# ------------------------------------------------------------
# STEP 4
# RUN SIMPLE EXPERIMENT
# ------------------------------------------------------------

capital = parameters["starting_capital"]
strategy_return = parameters["strategy_return"]

ending_capital = capital * (1 + strategy_return)
profit = ending_capital - capital
return_percent = (profit / capital) * 100

# ------------------------------------------------------------
# STEP 5
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
# STEP 6
# COPY IMPORTANT FILES
# ------------------------------------------------------------

shutil.copy("parameters.json", current_experiment / "parameters.json")
shutil.copy("hello.py", current_experiment / "hello.py")

# ------------------------------------------------------------
# STEP 7
# UPDATE LEADERBOARD
# ------------------------------------------------------------
#
# We still read + rewrite the whole CSV (simple and fine for a single
# appended row), but the ID itself is now collision-proof, and the
# workflow (see fixed .yml) pulls the latest leaderboard.csv and
# retries the push if the remote moved in the meantime. That combo
# is what actually prevents lost/duplicate rows end-to-end.

leaderboard_file = Path("leaderboard.csv")

rows = []

if leaderboard_file.exists():
    with leaderboard_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("experiment_id"):
                rows.append(row)

# Guard against ever appending a duplicate ID to the CSV itself,
# even though experiment_id generation is now collision-proof.
existing_ids = {row["experiment_id"] for row in rows}
if experiment_id not in existing_ids:
    rows.append(
        {
            "experiment_id": experiment_id,
            "return_percent": round(return_percent, 2),
            "profit": round(profit, 2),
            "status": "completed",
        }
    )
else:
    print(f"WARNING: {experiment_id} already in leaderboard.csv, skipping append.")

with leaderboard_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["experiment_id", "return_percent", "profit", "status"],
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
