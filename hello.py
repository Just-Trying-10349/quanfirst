# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 4
# ============================================================
#
# PURPOSE:
#
# We are introducing PARAMETERS.
#
# Instead of putting experiment settings directly inside
# our Python code, we store them separately in:
#
#     parameters.json
#
#
# The architecture is now:
#
# parameters.json
#       ↓
# hello.py
#       ↓
# experiment
#       ↓
# results
#
#
# Eventually:
#
# AI / optimizer
#       ↓
# parameters.json
#       ↓
# VectorBT
#       ↓
# backtest
#       ↓
# metrics
#       ↓
# compare experiments
#
# ============================================================


import json
from datetime import datetime
from pathlib import Path


print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 4")
print("=" * 70)


# ------------------------------------------------------------
# STEP 1 — FIND PARAMETERS FILE
# ------------------------------------------------------------

parameters_file = Path("parameters.json")


if not parameters_file.exists():

    raise FileNotFoundError(
        "parameters.json was not found."
    )


print()
print("Parameters file found:")
print(parameters_file)


# ------------------------------------------------------------
# STEP 2 — LOAD PARAMETERS
# ------------------------------------------------------------

with parameters_file.open("r", encoding="utf-8") as file:

    parameters = json.load(file)


print()
print("PARAMETERS")
print("-" * 70)

for name, value in parameters.items():

    print(f"{name}: {value}")


# ------------------------------------------------------------
# STEP 3 — READ EXPERIMENT SETTINGS
# ------------------------------------------------------------

strategy_name = parameters["strategy_name"]

starting_capital = parameters["starting_capital"]

strategy_return = parameters["strategy_return"]


# ------------------------------------------------------------
# STEP 4 — RUN EXPERIMENT
# ------------------------------------------------------------

ending_capital = (
    starting_capital *
    (1 + strategy_return)
)

profit = (
    ending_capital -
    starting_capital
)

return_percent = (
    profit /
    starting_capital
) * 100


# ------------------------------------------------------------
# STEP 5 — DISPLAY RESULTS
# ------------------------------------------------------------

print()
print("EXPERIMENT RESULTS")
print("-" * 70)

print(f"Strategy         : {strategy_name}")
print(f"Starting capital : ${starting_capital:,.2f}")
print(f"Ending capital   : ${ending_capital:,.2f}")
print(f"Profit           : ${profit:,.2f}")
print(f"Return           : {return_percent:.2f}%")

print("-" * 70)


# ------------------------------------------------------------
# STEP 6 — SAVE RESULTS
# ------------------------------------------------------------

result_file = Path("experiment_result.txt")


with result_file.open("w", encoding="utf-8") as file:

    file.write("QUANT RESEARCH EXPERIMENT\n")

    file.write("=" * 70 + "\n")

    file.write(
        f"Experiment time: "
        f"{datetime.now().isoformat()}\n"
    )

    file.write("\n")

    file.write("PARAMETERS\n")

    file.write("-" * 70 + "\n")

    for name, value in parameters.items():

        file.write(
            f"{name}: {value}\n"
        )

    file.write("\n")

    file.write("RESULTS\n")

    file.write("-" * 70 + "\n")

    file.write(
        f"Starting capital: "
        f"{starting_capital}\n"
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
        f"Return percent: "
        f"{return_percent}\n"
    )


# ------------------------------------------------------------
# STEP 7 — VERIFY RESULT
# ------------------------------------------------------------

print()
print("CHECKING RESULT FILE...")


if result_file.exists():

    print(
        "SUCCESS: experiment_result.txt was created."
    )

else:

    raise FileNotFoundError(
        "experiment_result.txt was not created."
    )


# ------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------

print()
print("=" * 70)

print("LEVEL 4 EXPERIMENT COMPLETED SUCCESSFULLY")

print("=" * 70)

print()
print("We have now separated:")
print()
print("PARAMETERS")
print("    ↓")
print("CODE")
print("    ↓")
print("RESULT")
print()
print("This is the foundation of automated parameter search.")
