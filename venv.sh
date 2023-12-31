#!/bin/bash
# NOT NECESSARY WITH POETRY. JUST RUN `poetry shell`

# Legacy:
# Source this file to initialize the venv and install deps
# To generate a dev requirements, run:
# poetry export --without-hashes -o requirements.in
GIT_DIR="/home/${USER}/git/slapi"
VENV_DIR="${GIT_DIR}/slvenv"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"
HOST_PYTHON=`which python3`
PYTHON_VERS=`python3 --version`

if [[ ! -d ${VENV_DIR} ]]; then
  echo "Creating ${PYTHON_VERS} venv at ${VENV_DIR}"
  ${HOST_PYTHON} -m venv ${VENV_DIR}
fi

if [[ -f ${VENV_ACTIVATE} ]]; then
  set +x
  echo "Activating ${VENV_ACTIVATE}"
  source ${VENV_ACTIVATE}
  ./slvenv/bin/python3 -m pip install poetry
fi

