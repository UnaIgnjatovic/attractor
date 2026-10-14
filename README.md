# attractor

Running example of Lecture 4, "Reproducible Python environments", of the
C1 Research Computing course (MPhil in Data Intensive Science, University of
Cambridge). The project measures the cycle period of ten chemostat
predator-prey experiments and is small enough to be rebuilt from scratch in a
few minutes on a laptop or on a Linux workstation.

## Setup

```bash
git clone https://github.com/borisbolliet/attractor.git
cd attractor
source setup_env.sh          # python3.12 venv, locked packages, .env, Jupyter kernel
python analyse.py            # table of periods, results/periods.csv, results/periods.png
python ask_llm.py            # optional: two sentences about the table from a language model
```

`source setup_env.sh` takes about 12 s with a warm pip cache (lecture laptop,
Python 3.12.12) and 13 s on the workstation (Python 3.12.3). A second
`source setup_env.sh` only prints the environment report. The script must be
sourced: run as `./setup_env.sh` it stops with a one-line message, because a
script that runs in a child shell cannot activate a venv in the calling shell.
Python 3.12 is expected as `python3.12`; another interpreter is selected with
`PYTHON=/path/to/python3.12 source setup_env.sh`.

## Three layers of a reproducible environment

1. **Interpreter and packages.** `requirements.txt` is the hand-written
   specification (`numpy>=1.26`, `matplotlib>=3.8`, ...). `requirements-lock.txt`
   is the exact set of 52 packages, produced by `pip freeze` in a Python 3.12
   venv on 2026-10-14; it is what `setup_env.sh` installs. The venv itself,
   `.venv/`, is a build product and is not committed.
2. **Configuration.** `.env.example` lists every variable the scripts read
   (`DATA_PATH`, `RESULTS_PATH`, `OMP_NUM_THREADS`, `MPLBACKEND`, `LLM_BASE_URL`,
   `LLM_API_KEY`, `LLM_MODEL`) with a default and a one-line comment.
   `setup_env.sh` copies it to `.env`, which is ignored by git and holds the
   local values; the scripts read `.env` with `python-dotenv`. A variable set
   in the shell takes precedence over `.env`, so
   `RESULTS_PATH=/tmp/out python analyse.py` writes elsewhere without editing
   the file.
3. **The setup script.** `setup_env.sh` turns the two files above into a
   working shell: it creates `.venv` with `python3.12`, activates it, installs
   the lock, creates `.env` if missing, exports its variables
   (`set -a; . ./.env; set +a`), registers the Jupyter kernel `attractor`
   and prints `check_env.py`.

## Files

| File | Role |
|---|---|
| `data/C1.csv` ... `data/C10.csv` | the ten runs; columns: time (days), algae (10^6 cells/ml), rotifers (animals/ml), egg ratio, eggs, dead animals, medium |
| `analyse.py` | period of every run from the peaks of the algae density; writes `results/periods.csv` and `results/periods.png` |
| `period.py` | the same computation for one run: `python period.py data/C9.csv` |
| `check_env.py` | interpreter, NumPy version and location, and the project variables |
| `ask_llm.py` | sends `results/periods.csv` to an OpenAI-compatible endpoint (`LLM_BASE_URL`) and prints a two-sentence description |
| `requirements.txt` | package specification |
| `requirements-lock.txt` | exact versions, `pip freeze`, Python 3.12 |
| `.env.example` | configuration template; copied to `.env` by `setup_env.sh` |
| `setup_env.sh` | one-step setup, to be sourced |
| `.gitignore` | `.venv/`, `.env`, `results/`, `__pycache__/`, `.ipynb_checkpoints/` |

## Why Python 3.12

The course interpreter is Python 3.13. The scripts were written in 2024 against
NumPy 1.26, and the lock pins `numpy==1.26.4`, the last 1.x release. NumPy
1.26.4 ships wheels for Python 3.9 to 3.12 only. On Python 3.13,
`pip install --only-binary=:all: -r requirements-lock.txt` stops with
`ERROR: No matching distribution found for numpy==1.26.4`; without
`--only-binary`, pip downloads `numpy-1.26.4.tar.gz` (15.8 MB) and compiles
it, which took 21 s on the lecture laptop and fails on a machine without a
C compiler.
With the loose `requirements.txt` instead, pip resolves `numpy>=1.26` to the
newest NumPy 2.x, and `analyse.py` stops with

```
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.
```

Replacing `np.NaN` by `np.nan` makes the script run under NumPy 2, with the
same table on screen and different digits in `results/periods.csv`:
`C9,141,17,8.059374809265137` under NumPy 1.26.4 and `C9,141,17,8.059375`
under NumPy 2.5.4. The data are loaded as `float32`; the period is a
`float32` scalar divided by a Python `int`, which NumPy 1 promotes to
`float64` and NumPy 2 keeps in `float32` (NEP 50). Pinning the interpreter
and the lock is what keeps the 2024 numbers.

## Method

The algae density of each run is read with `numpy.genfromtxt`; samples
recorded as `NaN` are dropped. A peak is a local maximum above the run's mean
density, at least three days after the previous peak. The period is the time
between the first and the last peak divided by the number of intervals. For
C9 (141 samples, 17 peaks) this gives 8.059 days, the period of the nutrient
pulses in that run.

## Data

The ten runs C1 to C10 are the chemostat experiments of B. Blasius, L. Rudolf,
G. Weithoff, U. Gaedke and G. F. Fussmann, *Long-term cyclic persistence in an
experimental predator-prey system*, Nature **577**, 226-230 (2020),
<https://www.nature.com/articles/s41586-019-1857-0>; data set on figshare,
doi:10.6084/m9.figshare.10045976, <https://doi.org/10.6084/m9.figshare.10045976>
(CC BY 4.0).

## Licence

MIT, Boris Bolliet 2026 (see `LICENSE`); the data keep their CC BY 4.0 licence.
