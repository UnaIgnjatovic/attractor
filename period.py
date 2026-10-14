"""Cycle period of one chemostat run.

Usage: python period.py data/C9.csv
"""
import sys

from analyse import cycle_period, load_run

if len(sys.argv) != 2:
    raise SystemExit("usage: python period.py <run.csv>")

t, algae = load_run(sys.argv[1])
period, peak_times = cycle_period(t, algae)
print(f"{sys.argv[1]}: {len(t)} samples, {len(peak_times)} peaks, period {period:.3f} days")
