#!/bin/bash
set -eu

echo '# WDI CSV file layouts'
echo
echo '[CSV download](https://databank.worldbank.org/data/download/WDI_CSV.zip)'
echo

for f in data/input/WDI_CSV/WDI{C,S}*.csv; do
    echo "## $f";
    echo;
    echo '```';
    head "$f" | tr -d '\r';
    echo '...';
    tail "$f" | tr -d '\r';
    echo '```';
    echo
done

