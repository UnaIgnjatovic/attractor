#!/usr/bin/env bash
# setup_env.sh -- virtual environment, locked packages, .env and Jupyter kernel
# of the attractor project, in one step.
#
# Usage, from the repository root, in bash or zsh:
#     source setup_env.sh
# Interpreter: python3.12 by default; PYTHON=/path/to/python3.12 source setup_env.sh
# overrides it. Running the script twice does nothing new and prints only the report.
# After editing .env, source the script again: the shell keeps the variables it exported.

# Sourced or run: only a sourced script can activate the venv in the calling shell.
if [ -n "${ZSH_VERSION:-}" ]; then
    case "$ZSH_EVAL_CONTEXT" in
        *:file) ;;
        *) echo "setup_env.sh: use 'source setup_env.sh'; a script that is run cannot activate the venv in the calling shell"; exit 1 ;;
    esac
elif [ -n "${BASH_VERSION:-}" ]; then
    if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
        echo "setup_env.sh: use 'source setup_env.sh'; a script that is run cannot activate the venv in the calling shell"
        exit 1
    fi
fi

setup_env() {
    local python="${PYTHON:-python3.12}"

    [ -f requirements-lock.txt ] || { echo "setup_env.sh: run it from the repository root"; return 1; }

    if [ ! -d .venv ]; then
        command -v "$python" >/dev/null 2>&1 \
            || { echo "setup_env.sh: $python not found; install Python 3.12 or set PYTHON"; return 1; }
        echo "setup_env.sh: creating .venv with $("$python" --version) at $(command -v "$python")"
        "$python" -m venv .venv || return 1
    fi

    . .venv/bin/activate || return 1

    # packages and kernel are installed once per venv; a newer lock file triggers a reinstall
    if [ ! -f .venv/lock.stamp ] || [ requirements-lock.txt -nt .venv/lock.stamp ]; then
        echo "setup_env.sh: installing requirements-lock.txt"
        python -m pip install --quiet --disable-pip-version-check -r requirements-lock.txt || return 1
        python -m ipykernel install --user --name attractor-py312 --display-name "Python (attractor 3.12)" >/dev/null || return 1
        echo "setup_env.sh: Jupyter kernel 'attractor-py312' -> $PWD/.venv/bin/python"
        touch .venv/lock.stamp
    fi

    if [ ! -f .env ]; then
        cp .env.example .env
        echo "setup_env.sh: .env created from .env.example; edit it to set LLM_BASE_URL"
    fi
    set -a
    . ./.env
    set +a

    python check_env.py
}

setup_env
