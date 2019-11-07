#!/bin/sh
# bash run.sh constraints_testK1.txt prefs_testK1.txt output_testK1.txt
echo ""
python3 registrarGroupProject.py $1 $2 $3
perl is_valid.pl $1 $2 $3
echo ""
echo ""
