# ============================================================
# QUANT RESEARCH AUTOMATION — LEVEL 7
# ============================================================
#
# GitHub
#    ↓
# GitHub Actions
#    ↓
# Python experiment
#    ↓
# Experiment ID
#    ↓
# Result
#    ↓
# Leaderboard
#    ↓
# Best experiment
#
# AI IS NOT CONNECTED YET.
#
# Later:
#
# GitHub Actions
#       ↓
# Python / VectorBT
#       ↓
# Many experiments
#       ↓
# leaderboard.csv
#       ↓
# External AI API
#       ↓
# AI analysis
#       ↓
# Improved parameters
#
# ============================================================


name: Quant Research Test


# ============================================================
# WORKFLOW TRIGGERS
# ============================================================

on:

  # Run when repository changes
  push:

  # Allow manual execution
  workflow_dispatch:

    inputs:

      force_rerun:

        description: "Run even if parameters.json has not changed"

        required: false

        type: boolean

        default: false


# ============================================================
# PERMISSIONS
# ============================================================

permissions:

  contents: write


# ============================================================
# CONCURRENCY
# ============================================================
#
# Only one experiment workflow can modify the repository
# at a time.
#
# This protects leaderboard.csv from simultaneous writes.
#
# ============================================================

concurrency:

  group: quant-research-experiments

  cancel-in-progress: false


# ============================================================
# JOBS
# ============================================================

jobs:

  run-python:

    runs-on: ubuntu-latest


    steps:


      # ======================================================
      # STEP 1
      # GET REPOSITORY
      # ======================================================

      - name: Step 1 - Get repository

        uses: actions/checkout@v5


      # ======================================================
      # STEP 2
      # INSTALL PYTHON
      # ======================================================

      - name: Step 2 - Setup Python

        uses: actions/setup-python@v6

        with:

          python-version: "3.12"


      # ======================================================
      # STEP 3
      # RUN EXPERIMENT
      # ======================================================

      - name: Step 3 - Run research experiment

        env:

          FORCE_RERUN: ${{ github.event.inputs.force_rerun || 'false' }}

        run: |

          python hello.py


      # ======================================================
      # STEP 4
      # SHOW EXPERIMENT OUTPUT
      # ======================================================

      - name: Step 4 - Check experiment output

        run: |

          echo ""
          echo "======================================================"
          echo "EXPERIMENT OUTPUT"
          echo "======================================================"

          echo ""

          echo "Experiment directories:"

          ls -R experiments || echo "(no new experiment created)"

          echo ""

          echo "======================================================"
          echo "LEADERBOARD"
          echo "======================================================"

          if [ -f leaderboard.csv ]; then

            cat leaderboard.csv

          else

            echo "leaderboard.csv does not exist."

            exit 1

          fi


      # ======================================================
      # STEP 5
      # SHOW CURRENT CHAMPION
      # ======================================================

      - name: Step 5 - Show research champion

        run: |

          echo ""
          echo "======================================================"
          echo "CURRENT BEST EXPERIMENT"
          echo "======================================================"

          echo ""

          if [ -f best_experiment.json ]; then

            cat best_experiment.json

          else

            echo "best_experiment.json was not created."

            exit 1

          fi

          echo ""

          echo "======================================================"


      # ======================================================
      # STEP 6
      # SAVE COMPLETE EXPERIMENT ARCHIVE
      # ======================================================

      - name: Step 6 - Save experiment archive

        uses: actions/upload-artifact@v4

        with:

          name: experiment-history-${{ github.run_id }}

          path: |

            experiments/

            leaderboard.csv

            best_experiment.json


      # ======================================================
      # STEP 7
      # SAVE RESEARCH MEMORY BACK TO GITHUB
      # ======================================================

      - name: Step 7 - Commit experiment memory

        run: |

          git config --global user.name "github-actions"

          git config --global user.email "github-actions@github.com"


          git add leaderboard.csv best_experiment.json


          git commit \
            -m "Update experiment research memory (${{ github.run_id }})" \
            || echo "No changes to commit"


          for attempt in 1 2 3 4 5; do

            git pull --rebase origin "${GITHUB_REF_NAME}" \
              && git push \
              && break

            echo "Push attempt $attempt failed, retrying..."

            sleep $((RANDOM % 5 + 1))

          done


      # ======================================================
      # STEP 8
      # FINAL SUCCESS MESSAGE
      # ======================================================

      - name: Step 8 - Complete

        run: |

          echo ""

          echo "======================================================"

          echo "QUANT RESEARCH LEVEL 7 COMPLETE"

          echo "======================================================"

          echo ""

          echo "The system now maintains:"

          echo ""

          echo "1. Individual experiment IDs"

          echo "2. Individual experiment folders"

          echo "3. Exact parameters"

          echo "4. Exact Python code"

          echo "5. Experiment results"

          echo "6. Experiment leaderboard"

          echo "7. Current best experiment"

          echo ""

          echo "AI is intentionally NOT connected yet."

          echo ""

          echo "Future architecture:"

          echo "Python / VectorBT"

          echo "       ↓"

          echo "Many experiments"

          echo "       ↓"

          echo "Leaderboard"

          echo "       ↓"

          echo "External AI API"

          echo "       ↓"

          echo "Research analysis"

          echo "       ↓"

          echo "Improved experiments"

          echo ""

          echo "======================================================"
