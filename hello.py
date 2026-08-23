# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 5
# ============================================================
#
# NEW FEATURE:
#
# Every experiment receives a unique ID.
#
# Architecture:
#
# parameters.json
#        |
#        v
# hello.py
#        |
#        v
# EXPERIMENT ID
#        |
#        v
# results folder
#
#
# This prevents experiment history from being lost.
#
# ============================================================


import json
from datetime import datetime
from pathlib import Path


print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 5")
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
# CREATE EXPERIMENT ID
# ------------------------------------------------------------


experiment_folder = Path("experiments")


experiment_folder.mkdir(exist_ok=True)


# Count existing experiments

existing = list(experiment_folder.glob("EXP-*"))


experiment_number = len(existing) + 1


experiment_id = (
    f"EXP-{experiment_number:04d}"
)


print()

print("Experiment ID:")
print(experiment_id)



# ------------------------------------------------------------
# STEP 3
# CREATE EXPERIMENT DIRECTORY
# ------------------------------------------------------------


current_experiment = (
    experiment_folder /
    experiment_id
)


current_experiment.mkdir()


print()

print("Experiment folder created:")

print(current_experiment)



# ------------------------------------------------------------
# STEP 4
# RUN SIMPLE EXPERIMENT
# ------------------------------------------------------------


capital = parameters["starting_capital"]

strategy_return = parameters["strategy_return"]


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



# ------------------------------------------------------------
# STEP 5
# SAVE RESULT
# ------------------------------------------------------------


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
        f"Experiment ID: {experiment_id}\n"
    )


    file.write(
        f"Time: {datetime.now()}\n\n"
    )


    file.write(
        "PARAMETERS\n"
    )


    for key,value in parameters.items():

        file.write(
            f"{key}: {value}\n"
        )


    file.write("\nRESULTS\n")


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



# ------------------------------------------------------------
# STEP 6
# COPY IMPORTANT FILES
# ------------------------------------------------------------


import shutil


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

# ------------------------------------------------------------
# STEP 7
# UPDATE LEADERBOARD
# ------------------------------------------------------------

import csv


leaderboard_file = Path("leaderboard.csv")


file_exists = leaderboard_file.exists()


with leaderboard_file.open(
    "a",
    newline="",
    encoding="utf-8"
) as file:


    writer = csv.writer(file)


    if not file_exists:

        writer.writerow(
            [
                "experiment_id",
                "return_percent",
                "profit",
                "status"
            ]
        )


    writer.writerow(
        [
            experiment_id,
            round(return_percent,2),
            round(profit,2),
            "completed"
        ]
    )


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
