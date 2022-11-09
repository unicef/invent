#!/usr/bin/bash
py.test --full-trace --timeout=180 --cov --cov-report html --cov-fail-under $1 --cov-report term-missing --cov-config .coveragerc 2>&1 | tee tests_output.txt
if grep "Total coverage: $1.00%" tests_output.txt; then
  exit 0;
else
  exit 1;
fi


