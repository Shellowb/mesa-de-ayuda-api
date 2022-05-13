#!/bin/sh
# Note: Call it from dev parent folder ../dev
# as dev/py_req.sh

pip freeze > dev/dev_requirements.txt
python --version > dev/runtime.txt