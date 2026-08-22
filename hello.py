# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 3
# ============================================================
#
# PURPOSE:
# Demonstrate the basic structure of a quantitative experiment:
#
# Python
#   ↓
# Experiment
#   ↓
# Metrics
#   ↓
# Saved result
#
# Later this will become:
#
# Strategy
#   ↓
# VectorBT
#   ↓
# Backtest
#   ↓
# Metrics
#   ↓
# Saved experiment
#
# ============================================================

from datetime import datetime
from pathlib import Path


print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 3")
print("=" * 70)


# ------------------------------------------------------------
# 1. EXPERIMENT PARAMETERS
# ------------------------------------------------------------

starting_capital = 10_000

strategy_return = 0.15


# ------------------------------------------------------------
# 2. CALCULATE RESULTS
# ------------------------------------------------------------

ending_capital = starting_capital * (1 + strategy_return)

profit = ending_capital - starting_capital

return_percent = (profit / starting_capital) * 100


# ------------------------------------------------------------
# 3. DISPLAY RESULTS
# ------------------------------------------------------------

print()
print("EXPERIMENT RESULTS")
print("-" * 70)

print(f"Starting capital : ${starting_capital:,.2f}")
print(f"Ending capital   : ${ending_capital:,.2f}")
print(f"Profit           : ${profit:,.2f}")
print(f"Return           : {return_percent:.2f}%")

print("-" * 70)


# ------------------------------------------------------------
# 4. CREATE RESULT FILE
# ------------------------------------------------------------

result_file = Path("experiment_result.txt")

with result_file.open("w", encoding="utf-8") as file:

    file.write("QUANT RESEARCH EXPERIMENT\n")
    file.write("=" * 70 + "\n")

    file.write(f"Time: {datetime.now().isoformat()}\n")
    file.write(f"Starting capital: {starting_capital}\n")
    file.write(f"Ending capital: {ending_capital}\n")
    file.write(f"Profit: {profit}\n")
    file.write(f"Return percent: {return_percent}\n")


# ------------------------------------------------------------
# 5. VERIFY THE FILE EXISTS
# ------------------------------------------------------------

print()
print("CHECKING RESULT FILE...")

if result_file.exists():

    print("SUCCESS: experiment_result.txt was created.")

    print()
    print("FILE CONTENTS")
    print("-" * 70)

    print(result_file.read_text(encoding="utf-8"))

else:

    print("ERROR: experiment_result.txt was NOT created.")

    raise FileNotFoundError(
        "experiment_result.txt was expected but does not exist."
    )


print("=" * 70)
print("EXPERIMENT COMPLETED SUCCESSFULLY")
print("=" * 70)
