# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 3
# ============================================================
#
# PURPOSE:
# Prove that GitHub Actions can:
#
# 1. Run Python
# 2. Perform a simple experiment
# 3. Calculate measurable results
# 4. Save those results to a file
#
# EVENTUAL SYSTEM:
#
# Strategy
#     ↓
# Backtest
#     ↓
# Metrics
#     ↓
# Save experiment
#     ↓
# Compare with previous experiments
#
# ============================================================


print("=" * 70)
print("QUANT RESEARCH EXPERIMENT — LEVEL 3")
print("=" * 70)


# ------------------------------------------------------------
# EXPERIMENT SETTINGS
# ------------------------------------------------------------

starting_capital = 10_000

strategy_return = 0.15

ending_capital = starting_capital * (1 + strategy_return)


# ------------------------------------------------------------
# CALCULATE SIMPLE METRICS
# ------------------------------------------------------------

profit = ending_capital - starting_capital

return_percent = (profit / starting_capital) * 100


# ------------------------------------------------------------
# DISPLAY RESULTS
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
# SAVE RESULTS
# ------------------------------------------------------------

with open("experiment_result.txt", "w") as file:

    file.write("QUANT RESEARCH EXPERIMENT\n")
    file.write("=" * 70 + "\n")

    file.write(f"Starting capital: {starting_capital}\n")
    file.write(f"Ending capital: {ending_capital}\n")
    file.write(f"Profit: {profit}\n")
    file.write(f"Return percent: {return_percent}\n")


print()
print("RESULT SAVED:")
print("experiment_result.txt")

print("=" * 70)
