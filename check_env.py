"""Report of the active environment: interpreter, NumPy, and the project variables.

Usage: python check_env.py
"""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

try:
    import numpy
    numpy_version, numpy_file = numpy.__version__, numpy.__file__
except ImportError:
    numpy_version = numpy_file = "not installed"

print(f"{'python':<16}{sys.executable}")
print(f"{'version':<16}{sys.version.split()[0]}")
print(f"{'numpy':<16}{numpy_version}")
print(f"{'numpy file':<16}{numpy_file}")
print(f"{'PYTHONPATH':<16}{os.environ.get('PYTHONPATH', '(unset)')}")

defaults = {
    "DATA_PATH": "data",
    "RESULTS_PATH": "results",
    "OMP_NUM_THREADS": "(unset: all cores)",
    "MPLBACKEND": "(unset: Agg in analyse.py)",
    "LLM_BASE_URL": "(unset)",
    "LLM_MODEL": "(unset)",
}
for name, default in defaults.items():
    print(f"{name:<16}{os.environ.get(name, default)}")
print(f"{'LLM_API_KEY':<16}{'set' if os.environ.get('LLM_API_KEY') else 'not set'}")
